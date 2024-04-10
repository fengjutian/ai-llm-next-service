from typing import Union

from openai import OpenAI 

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

class Item(BaseModel):
    ask: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat/")
async def read_chat(item: Item):
    print(item)

    client = OpenAI(
        api_key="sk-T6tYpWV2I50PlAVTPsIRFiFeOIxMNgtBc9kBjzAaD0azyAYr",
        base_url="https://api.moonshot.cn/v1",
    )
    
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": item.ask}
        ],
        temperature=0.3,
    )
    
    print(completion.choices)

    responseObj = {
        "msg": completion.choices[0].message
    }

    return responseObj

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/page/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """