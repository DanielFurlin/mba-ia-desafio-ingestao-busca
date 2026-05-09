import os

from dotenv import load_dotenv
from vector_store import get_vector_store
from search import RAG_PROMPT
from langchain.chat_models import init_chat_model

load_dotenv()

def main() -> None:
  chat_model = init_chat_model(model=os.getenv("CHATBOT_MODEL"))
  vector_store = get_vector_store()
  chain = RAG_PROMPT | chat_model
  try:
    while True:
      question = input("Faça sua pergunta: ")
      if not question or question.lower() in ["exit", "sair", "fim"]:
        break
      results = vector_store.similarity_search_with_score(question, k=10)
      answer = chain.invoke({"contexto": results, "pergunta": question})
      print(answer.content)
  except EOFError:
    pass
  finally:
    print("\nEncerrando o programa.")

if __name__ == "__main__":
  main()