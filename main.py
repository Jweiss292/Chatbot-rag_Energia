from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

# Caminho local do vector store
vector_store_path = './faiss_db'
print("🔍 Verificando vector store...")

try:
    if os.path.exists(vector_store_path):
        embedding_function = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
        db = FAISS.load_local(vector_store_path, embedding_function, allow_dangerous_deserialization=True)
        print("✅ Vector Store carregado.")
    else:
        print("⚠️ Vector Store não encontrado:", vector_store_path)
        db = None
except Exception as e:
    print("❌ Erro ao carregar vector store:", e)
    db = None

# Configura o LLM via OpenAI API
llm_gpt = None
if os.getenv("OPENAI_API_KEY"):
    try:
        llm_gpt = ChatOpenAI(model_name="gpt-4o-mini")
        print("✅ LLM carregado.")
    except Exception as e:
        print("❌ Erro ao configurar o LLM:", e)

# Monta pipeline RAG
rag_gpt = None
if db and llm_gpt:
    try:
        template_prompt = '''[INSTRUÇÕES]

Contexto:
- Você é especialista em regulamentação da REN 1000/2021 e tarifas de energia.
- Explique com clareza, adaptando a resposta para técnicos da CEMIG com conhecimento não especializado.

Documentos:
{context}

Pergunta:
{query}

Resposta:
'''
        prompt = PromptTemplate(input_variables=["context", "query"], template=template_prompt)

        def formatar_documentos(docs):
            return "\n\n".join(f"Fonte: {doc.metadata.get('fonte', 'desconhecida')}\nConteúdo: {doc.page_content}" for doc in docs)

        retriever = db.as_retriever(search_kwargs={"k": 10})
        rag_gpt = (
            {"context": retriever | formatar_documentos, "query": RunnablePassthrough()}
            | prompt
            | llm_gpt
            | StrOutputParser()
        )
        print("✅ RAG criada.")
    except Exception as e:
        print("❌ Erro ao criar RAG:", e)

# Inicia FastAPI com rota HTML e WebSocket
app = FastAPI()

html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Chatbot RAG</title>
    <style>
        body { font-family: sans-serif; background: #f0f0f0; padding: 20px; }
        #chat { background: white; padding: 15px; border-radius: 8px; max-width: 800px; margin: auto; height: 60vh; overflow-y: auto; }
        .msg { margin: 10px 0; padding: 8px; border-radius: 5px; }
        .user { background-color: #e2ffe2; text-align: right; }
        .bot { background-color: #e2e9ff; text-align: left; }
    </style>
</head>
<body>
    <h2>Chatbot RAG – REN 1000/2021</h2>
    <div id="chat"></div>
    <input type="text" id="input" placeholder="Digite uma pergunta..." style="width:80%;" />
    <button onclick="sendMessage()">Enviar</button>
    <script>
        const protocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
        const ws = new WebSocket(protocol + location.host + '/ws');

        ws.onmessage = function(event) {
            const msg = document.createElement("div");
            msg.className = "msg bot";
            msg.innerText = event.data;
            document.getElementById("chat").appendChild(msg);
        };

        function sendMessage() {
            const input = document.getElementById("input");
            const msg = document.createElement("div");
            msg.className = "msg user";
            msg.innerText = input.value;
            document.getElementById("chat").appendChild(msg);
            ws.send(input.value);
            input.value = "";
        }
    </script>
</body>
</html>
'''

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if rag_gpt:
                try:
                    response = rag_gpt.invoke(data)
                    await websocket.send_text(response)
                except Exception as e:
                    await websocket.send_text("Erro ao gerar resposta: " + str(e))
            else:
                await websocket.send_text("Chatbot indisponível no momento.")
    except Exception as e:
        print("📡 WebSocket encerrado:", e)
