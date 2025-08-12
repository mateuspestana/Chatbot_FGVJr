## Projeto de Chatbots — FGV Jr (Digital Development)

Este repositório foi criado para a formação ministrada à FGV Jr, na área de **Digital Development**, com foco no desenvolvimento de serviços de chatbot usando **Agno** (framework de agentes) e **Chainlit** (UI de chat para LLMs).

### O que está incluído
- **`app_basico.py`**: agente minimalista com Agno + Chainlit.
- **`app_rag.py`**: agente com RAG (bases: Wikipedia e opcionalmente textos em `txt_files/`) e **LanceDB** para armazenamento vetorial.
- **`app_yfinance.py`**: agente com ferramentas de finanças (preços com `yfinance` + calculadora) e instruções de formatação em tabela.

### Estrutura (resumo)
- `app_basico.py`, `app_rag.py`, `app_yfinance.py`
- `txt_files/` — textos para indexação (ex.: `jobs.txt`)
- `tmp/lancedb/` — base vetorial (persistência do LanceDB)
- `.chainlit/config.toml` — ajustes de UI e recursos do Chainlit
- `requirements.txt`

## Requisitos
- Python 3.12+
- Ambiente virtual recomendado (`.venv`)

Instale dependências:
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# No Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Chaves de API e configuração
Os exemplos usam modelos da **OpenAI** e da **Groq** via Agno.

- Defina as seguintes variáveis no shell antes de rodar (recomendado):
```bash
export OPENAI_API_KEY="sua_chave_openai"
export GROQ_API_KEY="sua_chave_groq"
```

- O código atual lê chaves de `utils.py` (constantes `OPENAI_API_KEY` e `api_key`). Para boas práticas, substitua por leitura via variáveis de ambiente (ou `.env`) e não versione segredos. Exemplo de `utils.py` seguro:
```python
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("GROQ_API_KEY")
```

> Importante: nunca suba chaves reais ao repositório.

## Como executar
Os três apps usam o Chainlit como servidor de chat.

- Rodar o app básico:
```bash
chainlit run app_basico.py -w
```

- Rodar o app com RAG (Wikipedia + LanceDB):
```bash
chainlit run app_rag.py -w
```
Ao iniciar, o app carrega/cria a base vetorial em `tmp/lancedb`. Ajuste fontes em `app_rag.py` (ex.: habilitar `TextKnowledgeBase` apontando para `txt_files/`).

- Rodar o app de finanças (yfinance):
```bash
chainlit run app_yfinance.py -w
```
Exemplo de prompt: “Qual o preço da ação da Apple?”

## Notas sobre cada app
- **Básico**: usa `Groq` via Agno para responder mensagens no chat.
- **RAG**: monta um `CombinedKnowledgeBase` (ex.: Wikipedia) e persiste embeddings no **LanceDB**. O parâmetro `recreate=True` força reindexação quando ajusta fontes.
- **YFinance**: utiliza `YFinanceTools` e `CalculatorTools` do Agno. A instrução do agente pede tabela com preço em USD e BRL (o agente consulta câmbio do dia para o cálculo em reais).

## Links de documentação
- **Agno (framework de agentes)**: `https://docs.agno.ai` (conceitos de `Agent`, modelos, ferramentas e knowledge bases)
- **Chainlit (UI de chat)**: `https://docs.chainlit.io`
- **LanceDB (vetor DB)**: `https://lancedb.com` • Docs: `https://lancedb.github.io/lancedb/`
- **OpenAI API**: `https://platform.openai.com/docs`
- **Groq (LLM inference)**: `https://console.groq.com/docs`
- **yfinance**: `https://pypi.org/project/yfinance/`
- **Sentence-Transformers**: `https://www.sbert.net/`
- **Wikipedia (referência)**: `https://www.wikipedia.org/`

## Dicas e boas práticas
- Use `.venv` dedicado ao projeto e congele versões se for publicar.
- Não versione chaves ou arquivos `.env`.
- Se mudar fontes de conhecimento em `app_rag.py`, mantenha `recreate=True` temporariamente para reindexar e depois troque para `False` para ganhar performance no boot.