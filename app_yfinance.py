from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.calculator import CalculatorTools
import chainlit as cl
from utils import api_key

agent = Agent(
    name="Agente de Finanças",
    tools=[YFinanceTools(stock_price=True), CalculatorTools()],
    model=Groq(id="openai/gpt-oss-120b", api_key=api_key),
    instructions="Use tabelas para exibir dados. Não inclua nenhum outro texto. Responda o preço em dólar e em reais brasileiros. Busque a cotação do dólar junto ao real para o cálculo do preço em reais.",
    markdown=True,
    debug_mode=False,
    show_tool_calls=False, # Mudar pra true se quiser ver as chamadas de ferramentas
)
# agent.print_response("Qual o preço da Ação da Apple?", stream=False)


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Oi! Pode me perguntar qualquer coisa relacionada a finanças e mercado de ações.").send()

@cl.on_message
async def on_message(message: cl.Message):
    reply = cl.Message(content="")
    await reply.send()

    stream = await agent.arun(message.content, stream=True)

    async for event in stream:
        text = getattr(event, "content", None)
        if text:
            await reply.stream_token(text)

    await reply.update()