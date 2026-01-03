# await cmd.send('you did not tell me what to reply with')
import asyncio

from twitchAPI.chat import Chat, ChatCommand, ChatMessage, ChatSub, EventData
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent


# TwitchAPI + EventSub Setup
async def twitch_event_loop():
    APP_ID = "APP_ID"
    APP_SECRET = "APP_SECRET"
    USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
    TARGET_CHANNEL = "revotopia"

    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    async def on_ready(ready_event: EventData):
        print("Bot is ready for work, joining channels")
        await ready_event.chat.join_room(TARGET_CHANNEL)

    async def on_message(msg: ChatMessage):
        print(f"in {msg.room.name}, {msg.user.name} said: {msg.text}")

    async def helpCommand(cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply("you did not tell me what to reply with")

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command("help", helpCommand)

    chat.start()

    try:
        input("press ENTER to stop \n")
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


await twitch_event_loop()
