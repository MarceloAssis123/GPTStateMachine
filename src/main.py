import asyncio
import openai
import os
import json
from dotenv import load_dotenv
import utils
import gptStateClassifier

# Carrega variáveis do arquivo .env
load_dotenv()

# Configure sua chave de API da OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

SellerStates = utils.States

HistoryStates = utils.HistoryState

global messages
messages = [
    {}
]

async def chamar_api(prompt: str) -> str:
    systemPrompt = f'''
        Você agora é um vendedor de Relogios suiços.

        Suas intruções são baseadas em estágios, aqui está o estágio atual da sua interação com o cliente.

        {json.dumps(SellerStates[HistoryStates[-1]]["SystemPrompt"])}

        Responda de acordo com o idioma do cliente
    '''

    messages[0] = {"role": "system", "content": systemPrompt}

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        conteudo =  response.choices[0].message.content
        return conteudo.strip()
    except Exception as e:
        return f"Ocorreu um erro ao chamar a API: {e}"

async def main():

    print("Welcome to the chat integrated with GPTStateMachine!")
    print("Type 'exit' to end the chat.\n")

    print(f"\n")
    print(f"Assistant: Hello, how are you?")
    messages.append({"role": "assistant", "content": 'Olá, tudo bem?'})
    
    while True:
        usuario = input("You: ")
        if usuario.strip().lower() in ["sair", "exit", "quit"]:
            print("Encerrando o chat. Até logo!")
            break

        # Adiciona a mensagem do usuário ao histórico.
        messages.append({"role": "user", "content": usuario})

        HistoryStates.append(await gptStateClassifier.GPTStateClassifier(HistoryStates, SellerStates, messages))
        
        # Chama a API com o histórico atualizado
        resposta_api = await chamar_api(messages)
        
        # Adiciona a resposta da API ao histórico
        messages.append({"role": "assistant", "content": f'{resposta_api}'})
        
        print(f"Assistant: {resposta_api}\n")

if __name__ == "__main__":
    asyncio.run(main())