from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage

from Chatbot_simples.llm import get_llm

llm = get_llm()

FAQ = {
    "horario": "Nosso horário de funcionamento é das 8h às 18h, de segunda a sexta.",
    "preco": "Nossos planos começam a partir de R$99 por mês.",
    "contato": "Você pode falar com nosso suporte pelo email suporte@empresa.com",
    "valor": "Nossos planos começam a partir de R$99 por mês.",   # sinônimo útil
    "preço": "Nossos planos começam a partir de R$99 por mês.",
}

# === Schema estruturado para classificação ===
class IntentClassification(BaseModel):
    """Classificação da intenção do usuário."""
    intent: Literal["saudacao", "faq", "suporte", "novo"] = Field(
        description="A intenção principal da mensagem do usuário. Deve ser exatamente uma das opções permitidas."
    )

def classify_node(state):
    """Classifica a intenção usando structured output (mais confiável)."""
    prompt = f"""
Você é um classificador de intenções para um chatbot de atendimento.

Analise a mensagem do usuário e classifique em **apenas uma** das seguintes intenções:

- saudacao: Cumprimentos, oi, olá, bom dia, etc.
- faq: Perguntas sobre horário, preço, planos, contato ou informações gerais da empresa.
- suporte: Pedidos de ajuda técnica, reclamações, problemas específicos.
- novo: Qualquer coisa que não se encaixe nas anteriores (ex: conversa casual, piada, spam, etc.).

Mensagem do usuário: "{state["user_message"]}"

Responda apenas com a classificação estruturada.
"""

    # Cria uma versão do LLM que sempre retorna o schema Pydantic
    structured_llm = llm.with_structured_output(IntentClassification)

    result: IntentClassification = structured_llm.invoke(prompt)

    return {"intent": result.intent}

def faq_node(state):
    faq_context = "\n".join([f"- {k}: {v}" for k, v in FAQ.items()])

    prompt = f"""Você é um assistente de atendimento. Responda a pergunta do usuário \
usando APENAS as informações do FAQ abaixo. Se a resposta não estiver no FAQ, \
diga que não tem essa informação e ofereça falar com um atendente.

FAQ:
{faq_context}

Pergunta: {state["user_message"]}"""

    response_text = llm.invoke(prompt).content.strip()
    return {"response": response_text}

def response_node(state):
    # Pega as últimas mensagens para o prompt (converte para texto)
    history_messages = state.get("history", [])[-30:]
    history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in history_messages[-30:]]
    )

    prompt = f"""
Você é um atendente profissional e educado de uma empresa de serviços.

Regras importantes:
- Seja sempre educado e direto
- Não invente informações
- Se não souber, ofereça falar com um atendente humano

Histórico da conversa:
{history_text}

Mensagem atual do cliente: {state["user_message"]}

Responda de forma natural e profissional:
"""

    response_text = llm.invoke(prompt).content.strip()
    return {"response": response_text}

def fallback_node(state):
    return {
        "response": (
            "Não entendi muito bem 🤔\n"
            "Pode reformular ou deseja falar com um atendente?"
        )
    }

def update_history_node(state):
    """Adiciona tanto a mensagem do usuário quanto a resposta do bot como mensagens reais."""
    updates = []

    # Adiciona a mensagem do usuário
    updates.append(HumanMessage(content=state["user_message"]))

    # Adiciona a resposta do bot (se existir)
    if state.get("response"):
        updates.append(AIMessage(content=state["response"]))

    return {"history": updates}   # add_messages vai cuidar do append
