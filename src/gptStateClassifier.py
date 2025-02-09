import openai
import os
import json
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configure sua chave de API da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI
global client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Definição do JSON Schema
JSON_SCHEMA = {
    "type": "json_schema",  # Indica que o formato de resposta é JSON Schema
    "json_schema": {
        "name": "GPTStateClassifierSchema",  # Nome identificador do schema
        "schema": {                # Aqui é definido o schema real
            "description": "Schema que define o próximo estado do vendedor baseado na conversa.",
            "type": "object",
            "properties": {
                "newState": {
                    "type": "string",
                    "description": "Uma string que informa o próximo estado do vendedor baseado na conversa."
                }
            },
            "required": ["newState"]
        }
    }
}

async def GPTStateClassifier(HistoryState, States, messages):
    EstadoAtual = HistoryState[-1]

    systemPrompt = f'''
    Você agora é um classificador de estados de máquina para uma AI de vendas.

    O estado atual da AI de vendas com essa interação com o cliente é {EstadoAtual}

    Analise todas as mensagens com o cliente para entender qual é o melhor próximo estado

    Aqui está as possibilidades de mundaça de estado com suas condições e novos estados. Não mude do estado atual se as condições não forem atingidas
    {json.dumps(States[EstadoAtual]["PossibleStateChange"])}
    '''

    messages[0] = {"role": "system", "content": systemPrompt}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format=JSON_SCHEMA,
    )
    
    result = json.loads(response.choices[0].message.content)

    newState = result["newState"]
    print(f'New State: {newState}')
    
    return newState