import chainlit as cl

from agno.agent import Agent
from agno.models.groq import Groq
from utils import api_key

# Agente básico
agent = Agent(
    name="AgnoChat",
    description="Um assistente minimal com Agno.",
    model=Groq(id="openai/gpt-oss-120b", api_key=api_key),
    markdown=True,  # O Chainlit renderiza markdown direitinho
)

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