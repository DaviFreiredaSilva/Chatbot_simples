from Chatbot_simples.graph import build_graph
import os
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# Carrega variáveis de ambiente (OpenAI key)
load_dotenv()

def main():
    print("🤖 Chatbot Simples - Modo Teste Local")
    print("Digite 'sair' ou 'exit' para encerrar.\n")
    
    conn = sqlite3.connect("Chatbot_simples/checkpoints.db", check_same_thread=False)
    checkpointer = SqliteSaver(conn)

    # Constrói o grafo uma única vez
    graph = build_graph(checkpointer=checkpointer)

    # Cada conversa tem um thread_id diferente
    thread_id = "teste-local-1"   # ← mude isso para testar múltiplos usuários
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"✅ Usando thread_id: {thread_id} (persistente no banco checkpoints.db)\n")
    
    while True:
        try:
            user_input = input("Você: ").strip()
            
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("👋 Encerrando o teste. Até mais!")
                break
                
            if not user_input:
                print("Por favor, digite uma mensagem.\n")
                continue
            
            # Executa o grafo
            result = graph.invoke(
                {"user_message": user_input},
                config=config
            )
            
            # Mostra a resposta do bot
            response = result.get("response", "Desculpe, não consegui gerar uma resposta.")
            print(f"Bot: {response}\n")
            
            # Mostrar a intenção detectada (útil para debug)
            intent = result.get("intent", "não detectada")
            print(f"[Debug] Intenção: {intent}\n")
            
        except Exception as e:
            print(f"❌ Erro durante a execução: {e}\n")
            # Continua o loop mesmo com erro

if __name__ == "__main__":
    main()