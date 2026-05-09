import os

from dotenv import load_dotenv
from pgvector_helper import get_pgvector
from search import search_prompt
from langchain.chat_models import init_chat_model

load_dotenv()

def main():
    try:
        while True:
            question = input("Faça sua pergunta: ")
            if not question or question.lower() in ["exit", "sair", "fim"]:
                break
            chat_model = init_chat_model(model=os.getenv("CHATBOT_MODEL"))
            pgvector = get_pgvector()
            results = pgvector.similarity_search_with_score(question, k=10)
            chain = search_prompt() | chat_model
            if not chain:
                print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
                return
            answer = chain.invoke({"contexto": results, "pergunta": question})
            print(answer.content)
    except EOFError:
        # Captura o Ctrl+D e finaliza o loop graciosamente
        pass
    finally:
        print("\nEncerrando o programa.")

if __name__ == "__main__":
    main()