from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from mysite.schemas.ai_schema import OrderCreateOutputSchema
from dotenv import load_dotenv
import os

load_dotenv()


order_parser = JsonOutputParser(pydantic_object=OrderCreateOutputSchema)
order_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Ты — AI-ассистент для оформления заказов службы доставки.

Твоя задача — извлечь из сообщения клиента ВСЕ товары, которые он хочет заказать.

ПРАВИЛА:
- Каждый отдельный товар добавляй как отдельный объект в items.
- Никогда не объединяй несколько разных товаров в один объект.
- Не пропускай товары, явно указанные клиентом.
- Определи название, категорию, характеристики и количество каждого товара.
- Если количество не указано, используй 1.
- Если цена не указана, используй null.
- Если цена указана, price — цена одной единицы товара.
- Если price известна, total_price = price * quantity.
- Если price неизвестна, total_price = null.
- Не придумывай отсутствующие характеристики или цены.

ЯЗЫК:
- Название, категория и описание должны быть на языке клиента.
- Если клиент пишет на кыргызском — используй кыргызский.
- Если клиент пишет на русском — используй русский.
- Если клиент пишет на английском — используй английский.

TITLE:
- Только название товара.
- Не добавляй количество, цену, размер или цвет.

DESCRIPTION:
- Указывай только характеристики, явно написанные клиентом.
- Например: размер, цвет, бренд, модель.

Верни ТОЛЬКО JSON:

{{
    "items": [
        {{
            "title": "название товара",
            "category": "категория",
            "description": "характеристики",
            "quantity": 1,
            "price": null,
            "total_price": null
        }}
    ]
}}

Каждый товар должен быть отдельным элементом списка items.
Не добавляй текст или markdown вне JSON.
"""
    ),
    (
        "human",
        "{text}"
    )
])

order_model = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_URL"),
    temperature=0,
    max_completion_tokens=500
)

order_parser = JsonOutputParser(pydantic_object=OrderCreateOutputSchema)
order_create_chain = order_prompt | order_model | order_parser