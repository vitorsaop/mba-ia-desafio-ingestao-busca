import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

# Validar variáveis de ambiente
for k in ("OPENAI_MODEL", "PGVECTOR_URL", "PGVECTOR_COLLECTION"):
    if not os.getenv(k):
        raise ValueError(f"Missing environment variable: {k}")


def search_documents(query: str, k: int = 10):
    """
    Busca documentos similares no banco de dados vetorial.
    
    Args:
        query: Pergunta ou texto para buscar
        k: Número de documentos mais relevantes a retornar (padrão: 10)
        
    Returns:
        Lista de tuplas (documento, score) ordenadas por relevância
    """
    try:
        # Configurar embeddings
        embeddings = OpenAIEmbeddings(
            model=os.getenv("OPENAI_MODEL", "text-embedding-3-small")
        )
        
        # Conectar ao PGVector
        store = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PGVECTOR_COLLECTION"),
            connection=os.getenv("PGVECTOR_URL"),
            use_jsonb=True,
        )
        
        # Realizar busca por similaridade
        results = store.similarity_search_with_score(query, k=k)
        
        return results
    
    except Exception as e:
        print(f"Erro ao buscar documentos: {e}")
        return []


def format_search_results(results):
    """
    Formata os resultados da busca para exibição.
    
    Args:
        results: Lista de tuplas (documento, score)
        
    Returns:
        String formatada com os resultados
    """
    if not results:
        return "Nenhum resultado encontrado."
    
    output = []
    for i, (doc, score) in enumerate(results, start=1):
        output.append("=" * 50)
        output.append(f"Resultado {i} (score: {score:.4f}):")
        output.append("=" * 50)
        output.append("\nTexto:\n")
        output.append(doc.page_content.strip())
        output.append("\n\nMetadados:")
        for k, v in doc.metadata.items():
            output.append(f"  {k}: {v}")
        output.append("\n")
    
    return "\n".join(output)


def get_context_from_results(results):
    """
    Extrai e concatena o contexto dos resultados da busca.
    
    Args:
        results: Lista de tuplas (documento, score)
        
    Returns:
        String com o contexto concatenado
    """
    if not results:
        return ""
    
    contexts = []
    for i, (doc, score) in enumerate(results, start=1):
        contexts.append(f"[Trecho {i}]:\n{doc.page_content.strip()}")
    
    return "\n\n".join(contexts)


if __name__ == "__main__":
    # Teste standalone do módulo de busca
    test_query = input("Digite sua pergunta: ").strip()
    
    if not test_query:
        print("Nenhuma pergunta fornecida.")
    else:
        print("\n🔍 Buscando documentos relevantes...\n")
        results = search_documents(test_query, k=10)
        
        if results:
            print(format_search_results(results))
        else:
            print("Não foi possível realizar a busca.")