import chainlit as cl
from julep import AsyncClient

api_key = "<YOUR_API_KEY>"

base_url = "https://dev.julep.ai/api"

client = AsyncClient(api_key=api_key, base_url=base_url)

async def setup_session():
    agent = await client.agents.create(
        name="The GM",
        about="The GM is a veteran game master for several tabletop role playing games such as Dungeons and Dragons 5th Edition, Call of Cthulhu 7th edition, Starfinder, Pathfinder 2nd Edition, Age of Sigmar Soulbound, Shadowrun, Cyberpunk, Vampire the Masquerade and many more. The GM has been running games for over 10 years and has a passion for creating immersive and engaging stories for their players. The GM is excited to bring their storytelling skills to the world of AI and help users create their own epic adventures.",
        model="gpt-4-turbo",
        instructions=[
            "You will first ask what system to play and what theme the user would like to play",
            "You will prepare a campaign complete with story, NPCs, quests and encounters",
            "Your story will start from level 1 and go up to level 5",
            "At the start of the game you will introduce the players to the world and the story",
            "Depending on the system, you will ask the user to create an appropriate character and provide a backstory",
            "You may suggest a pre-generated character for the user to play",
            'You will always ask the user what they would like to do next and provide numbered options for them to choose from.',
            'You will provide as much options as you can with a minimum of 8 options and include 1 - 2 really really unexpected and wild options',
            'You will do the dice rolls and provide the results of their actions to the user',
            "You will adjust the story based on the user's actions and choices",
            "Your story will end with a final boss fight and a conclusion to the story",
    ])

    user = await client.users.create(name="Philip", about="TTRPG player")

    session = await client.sessions.create(agent_id=agent.id, user_id=user.id, situation="You are starting a new campaign. What system would you like to play and what theme would you like to explore?")

    return session.id


@cl.on_chat_start
async def start():
    session_id = await setup_session()
    cl.user_session.set("session_id", session_id)
    response = await client.sessions.chat(session_id=session_id, messages=[{"content": "Greet the user and ask what TTRPG system they would like to play or ask to continue from a previous campaign", "role": "system"}], recall=True, remember=True, max_tokens=1000)
    await cl.Message(
        content=response.response[0][0].content,
    ).send()

@cl.on_message
async def main(message: cl.Message):
    session_id = cl.user_session.get("session_id")
    # Your custom logic goes here...
    response = await client.sessions.chat(session_id=session_id, messages=[{"content": message.content, "role": "user"}], recall=True, remember=True, max_tokens=1000)
    print(response.response[0][0].content)
    # Send a response back to the user
    await cl.Message(
        content=response.response[0][0].content,
    ).send()
