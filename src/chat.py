import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from search import search_documents, get_context_from_results

load_dotenv()

# Validar variáveis de ambiente
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Missing environment variable: OPENAI_API_KEY")


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda SOMENTE com base no CONTEXTO fornecido acima.
- Se a informação não estiver explicitamente no CONTEXTO, responda EXATAMENTE:
  "Não tenho informações necessárias para responder sua pergunta."
- NUNCA invente ou use conhecimento externo.
- NUNCA produza opiniões ou interpretações além do que está escrito no CONTEXTO.
- Seja preciso e objetivo, citando informações diretas do contexto.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO":
"""


def create_chat_chain():
    """
    Cria a chain de chat com LLM e prompt template.
    
    Returns:
        Chain configurada para responder perguntas com base no contexto
    """
    try:
        # Configurar o modelo LLM
        llm = ChatOpenAI(
            model="gpt-5-nano",
            temperature=0,  # Temperatura 0 para respostas mais determinísticas
        )
        
        # Criar o template de prompt
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        
        # Criar a chain: prompt -> LLM -> parser
        chain = prompt | llm | StrOutputParser()
        
        return chain
    
    except Exception as e:
        print(f"Erro ao criar chat chain: {e}")
        return None


def chat_with_context(question: str, chain, k: int = 10):
    """
    Processa uma pergunta: busca contexto relevante e gera resposta.
    
    Args:
        question: Pergunta do usuário
        chain: Chain do LangChain configurada
        k: Número de documentos a recuperar (padrão: 10)
        
    Returns:
        Resposta do LLM baseada no contexto
    """
    try:
        # 1. Buscar documentos relevantes no banco vetorial
        print("🔍 Buscando contexto relevante...")
        results = search_documents(question, k=k)
        
        if not results:
            return "Não foi possível encontrar informações relevantes no documento."
        
        # 2. Extrair e concatenar o contexto
        contexto = get_context_from_results(results)
        
        # 3. Invocar a chain com contexto e pergunta
        print("💭 Processando resposta...\n")
        resposta = chain.invoke({
            "contexto": contexto,
            "pergunta": question
        })
        
        return resposta
    
    except Exception as e:
        print(f"Erro ao processar pergunta: {e}")
        return "Ocorreu um erro ao processar sua pergunta."


def main():
    """
    Função principal que inicia o chat interativo CLI.
    """
    print("=" * 60)
    print("🤖 Chat RAG - Sistema de Perguntas e Respostas sobre PDF")
    print("=" * 60)
    print("\nBem-vindo! Faça perguntas sobre o conteúdo do documento.")
    print("Digite 'sair' ou 'exit' para encerrar.\n")
    
    # Criar a chain
    chain = create_chat_chain()
    
    if not chain:
        print("❌ Não foi possível iniciar o chat. Verifique as configurações.")
        return
    
    # Loop interativo
    while True:
        try:
            # Receber pergunta do usuário
            question = input("👤 Você: ").strip()
            
            # Verificar comandos de saída
            if question.lower() in ('sair', 'exit', 'quit', 'q'):
                print("\n👋 Até logo!")
                break
            
            # Ignorar perguntas vazias
            if not question:
                continue
            
            # Processar pergunta e obter resposta
            resposta = chat_with_context(question, chain, k=10)
            
            # Exibir resposta
            print(f"\n🤖 Assistente: {resposta}\n")
            print("-" * 60 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrompido. Até logo!")
            break
        
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}\n")


if __name__ == "__main__":
    main()