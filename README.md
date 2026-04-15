# Chatbot Simples com LangGraph

Um chatbot inteligente baseado em grafo de estados usando **LangGraph** e integração com LLM.  
Projeto desenvolvido para demonstrar conhecimentos em Python, automação de conversas e construção de agentes conversacionais.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-FF6F00?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)

## Sobre o Projeto

Este é um **chatbot simples porém bem arquitetado**, construído com abordagem de **grafo de estados** (State Machine).  
Em vez de usar apenas regras `if/else`, o projeto utiliza **LangGraph** para criar fluxos de conversa mais organizados, previsíveis e fáceis de manter.

O bot gerencia estados da conversa através de nós (`nodes`) e transições definidas em um grafo, permitindo expansão futura para fluxos complexos (ex: atendimento ao cliente, agendamento, suporte técnico, etc.).

### Principais Tecnologias

- **Python**
- **LangGraph** (construção de grafos de agentes)
- **LangChain** / Integração com LLM (`llm.py`)
- Gerenciamento de estado (`state.py`)
- Arquitetura modular com nós e grafo

## Funcionalidades

- Fluxo de conversa baseado em grafo de estados
- Gerenciamento inteligente do estado da conversa
- Integração com modelo de linguagem (LLM)
- Código limpo, modular e bem organizado
- Fácil de expandir com novos nós e fluxos

## Como Executar

### 1. Clone o repositório

bash
git clone https://github.com/DaviFreiredaSilva/Chatbot_simples.git
cd Chatbot_simples

### 2. Crie um ambiente virtual (recomendado)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

### 3. Instale as dependências
pip install -r requirements.txt
(Se ainda não tiver o arquivo requirements.txt, crie um com as principais dependências: langgraph, langchain, langchain-openai ou langchain-community, etc.)

### 4. Configure sua chave de API (se usar LLM)
Crie um arquivo .env na raiz do projeto e adicione sua chave:
env
OPENAI_API_KEY=sua_chave_aqui
# ou GROQ_API_KEY, ANTHROPIC_API_KEY, etc.

### 5. Execute o chatbot
python main.py
Ou, se preferir a versão com interface:
Bash
python app.py
Estrutura do Projeto
textChatbot_simples/
├── main.py          # Ponto de entrada principal
├── app.py           # Interface (console ou web)
├── graph.py         # Definição do grafo e fluxo
├── nodes.py         # Nós individuais da conversa
├── state.py         # Gerenciamento do estado
├── llm.py           # Configuração e chamada do LLM
├── __init__.py
└── README.md
O que aprendi / Habilidades demonstradas

Arquitetura de agentes conversacionais com LangGraph
Construção de grafos de estados para controle de fluxo
Boas práticas de modularização em Python
Integração com modelos de linguagem (LLM)
Organização de projetos para portfólio

Próximos Passos (Roadmap)

 Adicionar interface web com Streamlit ou Gradio
 Implementar memória de conversa persistente
 Criar múltiplos fluxos (ex: vendas, suporte, agendamento)
 Adicionar tratamento de intenções com RAG
 Deploy em plataforma (Railway, Render ou Hugging Face)

Contato
Desenvolvido por Davi Freire da Silva
Quer um chatbot personalizado para seu negócio?
Me chame no LinkedIn ou por e-mail!
