import chainlit as cl
from julep import AsyncClient

api_key = ""

base_url = "https://dev.julep.ai/api"
agent_id = "6693399d-c379-4199-83c3-9c62d03f8908"
user_id = "3563f0d2-cb4a-4e8a-851f-1fdc30fdd94c"
session_id = "79a2ca4f-a63f-4127-bd32-9295943d49d9"

client = AsyncClient(api_key=api_key, base_url=base_url)


@cl.on_chat_start
async def start():
    response = await client.sessions.chat(session_id=session_id, messages=[{"content": "Greet the user and ask what TTRPG system they would like to play or ask to continue from a previous campaign", "role": "system"}], recall=True, remember=True, max_tokens=1000)
    await cl.Message(
        content=response.response[0][0].content,
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    response = await client.sessions.chat(session_id=session_id, messages=[{"content": message.content, "role": "user"}], recall=True, remember=True, max_tokens=1000)
    print(response.response[0][0].content)
    # Send a response back to the user
    await cl.Message(
        content=response.response[0][0].content,
    ).send()
