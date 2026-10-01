from langchain.messages import AIMessage, HumanMessage, SystemMessage
from  langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview", temperature=0)

messages = [
    SystemMessage(
        content=(
            'Ты очень опытный python senior разработчик.'
            'Отвечаешь на вопросы кратко и сс примерпми.'
            'Ответ долден быть максимум 5 предложения.'
        )
    ),
    HumanMessage(
        content=('Что такое Langchain?')
    )
]

response = model.invoke(messages)

print(response.content)