

# await cmd.send('you did not tell me what to reply with')
import asyncio
import pygame
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent


# Pygame Game Logic
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("TwitchAPI + Pygame")
        self.font = pygame.font.SysFont(None, 40)
        self.redeem_count = 0
        self.running = True

    def on_redemption(self, reward_title: str):
        if reward_title.lower() == "jump":
            self.redeem_count += 1

    async def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((20, 20, 20))
            text = self.font.render(f"Jumps: {self.redeem_count}", True, (255, 255, 255))
            self.screen.blit(text, (100, 130))
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)

        pygame.quit()



# TwitchAPI + EventSub Setup
async def twitch_event_loop():

    APP_ID = 'APP_ID'
    APP_SECRET = 'APP_SECRET'
    USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
    TARGET_CHANNEL = 'revotopia'

    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    async def on_ready(ready_event: EventData):
        print('Bot is ready for work, joining channels')
        await ready_event.chat.join_room(TARGET_CHANNEL)

    async def on_message(msg: ChatMessage):
        print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')

    async def helpCommand(cmd: ChatCommand):
        if len(cmd.parameter) == 0:
            await cmd.reply('you did not tell me what to reply with')

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command('help', helpCommand)

    chat.start()

    try:
        input('press ENTER to stop \n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()
# Run both asyncio loops
async def main():
    game = Game()
    await asyncio.gather(
        twitch_event_loop(),
        game.run()
    )


if __name__ == '__main__':
    asyncio.run(main())
