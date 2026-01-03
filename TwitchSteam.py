# Pygame Game Logic
class Stream:
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

Live = Stream()
Live.run()

#Pygame Video Data To Flie
import pygame
import cv2
pygame.init()

screen  = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fourcc = cv2.VideoWriter.fourcc(*'XVID')
writer = cv2.VideoWriter('output.avi', fourcc, 60.0, (1280, 720))

game_Play = True

while game_Play:
    #GameDisplay
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), [100, 100, 400, 100], 2)
    #--------------------

    # Record PyGame Screen
    screen_data = pygame.surfarray.array3d(screen)
    frame = cv2.transpose(screen_data)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    writer.write(frame)
    #---------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_Play = False

    pygame.display.update()
    clock.tick(60)

writer.release()
pygame.quit()

#RTMP STREAMING
# GET https://ingest.twitch.tv/ingests
# rtmp://<ingest-server>/app/<stream-key>[?bandwidthtest=true]
# https://trac.ffmpeg.org/wiki/EncodingForStreamingSites

STREAM_KEY = "STREAM_KEY"  # <-- Replace this
TWITCH_URL = "TWITCH_URL"
WIDTH, HEIGHT = 640, 480
FRAME_RATE = 30
SAMPLE_RATE = 44100
AUDIO_CHANNELS = 2

