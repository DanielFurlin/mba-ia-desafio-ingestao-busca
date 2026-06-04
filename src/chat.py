from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from vector_store import get_vector_store
from search import RAG_PROMPT
from settings import settings
from dotenv import load_dotenv
load_dotenv()

def main() -> None:
    if settings.google_chatbot_model:
        chat_model = ChatGoogleGenerativeAI(model=settings.google_chatbot_model)
    elif settings.openai_chatbot_model:
        chat_model = ChatOpenAI(model=settings.openai_chatbot_model)
    else:
        raise ValueError("A variável de ambiente GOOGLE_CHATBOT_MODEL não está definida.")
    vector_store = get_vector_store()
    chain = RAG_PROMPT | chat_model
    try:
        while True:
            question = input("Faça sua pergunta[\"sair\" para finalizar]: ")
            if not question or question.lower() in ["exit", "sair", "fim"]:
                break
            results = vector_store.similarity_search_with_score(question, k=10)
            contexto = "\n\n".join(doc.page_content for doc, _ in results)
            answer = chain.invoke({"contexto": contexto, "pergunta": question})
            print(answer.content)
    except EOFError:
        pass
    finally:
        print("\nEncerrando o programa.")


if __name__ == "__main__":
    main()
