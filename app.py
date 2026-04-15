import os
import sqlite3
from fastapi import FastAPI, Request, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from Chatbot_simples.graph import build_graph
from twilio.request_validator import RequestValidator
from langgraph.checkpoint.sqlite import SqliteSaver

validator = RequestValidator(os.getenv("TWILIO_AUTH_TOKEN"))

#Conexão com sqlite para persistência dos checkpoints do grafo
conn = sqlite3.connect("Chatbot_simples/checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

app = FastAPI()
graph = build_graph(checkpointer=checkpointer)

@app.post("/webhook")
async def whatsapp_webhook(request: Request):

   # Ler form apenas uma vez
    form_data = await request.form()
    form_dict = dict(form_data)
    
    # url = str(request.url)
    # signature = request.headers.get("X-Twilio-Signature", "")

    # if not validator.validate(url, form_dict, signature):
    #     raise HTTPException(status_code=403, detail="Assinatura Twilio inválida.")

    user_id = form_data.get("From")
    config = {"configurable": {"thread_id": user_id}}

    user_message = form_data.get("Body") or ""

    if not user_message:
        # Resposta vazia para mensagens sem conteúdo
        return str(MessagingResponse())

    print("Realiando invoke")
    result = graph.invoke({
        "user_message": user_message},
        config=config
    )

    twilio_response = MessagingResponse()
    response_text = result.get("response") or "Desculpe, ocorreu um erro interno. Tente novamente."
    twilio_response.message(response_text)

    #Correção de formato para que o Twillio aceite a resposta
    return Response(
        content=str(twilio_response), 
        media_type="application/xml"
    )