Chatbot-rag_Energia/
├── main.py                 # Backend FastAPI + frontend HTML + WebSocket
├── requirements.txt        # Dependências do projeto
├── Procfile                # Instrução de inicialização para o Render
├── faiss_db/               # Base vetorial treinada
│   ├── index.faiss
│   └── index.pkl
├── README.md               # Documentação principal do projeto

# 🤖 Chatbot RAG – REN 1000/2021

Este é um chatbot construído com FastAPI, WebSocket e arquitetura RAG (Retrieval-Augmented Generation), treinado com documentos relacionados à **Resolução Normativa ANEEL nº 1000/2021**, focado em explicações para profissionais da área de energia, como os técnicos da CEMIG.

---

## ⚙️ Tecnologias utilizadas

- FastAPI + WebSocket
- LangChain (FAISS, PromptTemplate, RAG Pipeline)
- HuggingFace Embeddings (modelo `intfloat/multilingual-e5-large`)
- OpenAI GPT-4o-mini
- Base vetorial local em FAISS

---

## 📦 Estrutura do Projeto

hatbot-rag_Energia/ ├── main.py # Backend + frontend HTML via FastAPI ├── requirements.txt # Dependências do projeto ├── Procfile # Para deploy no Render ├── faiss_db/ # Base vetorial com os documentos indexados │ ├── index.faiss │ └── index.pkl


---

## ▶️ Como rodar localmente

1. Clone o repositório:

```bash
git clone https://github.com/Jweiss292/Chatbot-rag_Energia.git
cd Chatbot-rag_Energia


Crie um ambiente virtual (opcional):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

