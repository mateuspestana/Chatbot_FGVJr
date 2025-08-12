import chainlit as cl

from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.text import TextKnowledgeBase
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.wikipedia import WikipediaKnowledgeBase
from agno.embedder.openai import OpenAIEmbedder
from agno.models.openai import OpenAIChat
from utils import OPENAI_API_KEY, api_key

print("Carregando o modelo de embedding...")
# embedder = SentenceTransformerEmbedder(id="Qwen/Qwen3-Embedding-0.6B", api_key=api_key)
embedder = OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536, api_key=OPENAI_API_KEY)
llm = OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY)

print("Carregando o banco de dados...")
vector_db = LanceDb(
    table_name="dados",
    uri="tmp/lancedb",
    search_type=SearchType.vector,
    embedder=embedder
)

print("Carregando o banco de dados de URLs...")
# url_db = WebsiteKnowledgeBase(
#     name="URLs",
#     urls=["https://pt.wikipedia.org/wiki/Estado_Novo_(Brasil)", 
#           "https://pt.wikipedia.org/wiki/Era_Vargas",
#           "https://pt.wikipedia.org/wiki/Getúlio_Vargas"],
#     max_depth=2,
#     vector_db=vector_db,
# )
url_db = WikipediaKnowledgeBase(
    topics=["getulio vargas", "fernando henrique cardoso"],
    vector_db=vector_db,
)

print("Carregando o banco de dados de textos...")
text_db = TextKnowledgeBase(
    path="txt_files",
    vector_db=vector_db,
)

print("Carregando o banco de dados combinado...")
combined_db = CombinedKnowledgeBase(
    sources=[url_db, 
            #  text_db
             ],
    embedder=embedder,
    vector_db=vector_db,
    search_type=SearchType.vector,
)

print("Carregando o agente...")
agent = Agent(
    name="AgnoChat",
    description="Um assistente com Agno.",
    # model=Groq(id="openai/gpt-oss-120b", api_key=api_key),
    model=llm,
    markdown=True,  # O Chainlit renderiza markdown direitinho
    knowledge=combined_db,
    search_knowledge=True,
)
combined_db.load(recreate=True) # Aqui sempre botar True quando adicionar novas fontes

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Oi! Pode me perguntar qualquer coisa.").send()

@cl.on_message
async def on_message(message: cl.Message):
    reply = cl.Message(content="")
    await reply.send()

    # pega o stream assíncrono do Agno
    stream = await agent.arun(message.content, stream=True)

    # consome os eventos de forma assíncrona
    async for event in stream:
        text = getattr(event, "content", None)
        if text:
            await reply.stream_token(text)

    await reply.update()