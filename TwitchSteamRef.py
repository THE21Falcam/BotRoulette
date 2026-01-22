# Pygame Video Data To Flie
import cv2
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fourcc = cv2.VideoWriter.fourcc(*"XVID")
writer = cv2.VideoWriter("output.avi", fourcc, 60.0, (1280, 720))

game_Play = True

while game_Play:
    # GameDisplay
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), [100, 100, 400, 100], 2)
    # --------------------

    # Record PyGame Screen
    screen_data = pygame.surfarray.array3d(screen)
    frame = cv2.transpose(screen_data)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    writer.write(frame)
    # ---------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_Play = False

    pygame.display.update()
    clock.tick(60)

writer.release()
pygame.quit()

# RTMP STREAMING
# GET https://ingest.twitch.tv/ingests
# rtmp://<ingest-server>/app/<stream-key>[?bandwidthtest=true]
# https://trac.ffmpeg.org/wiki/EncodingForStreamingSites

STREAM_KEY = "STREAM_KEY"  # <-- Replace this
TWITCH_URL = "TWITCH_URL"
WIDTH, HEIGHT = 640, 480
FRAME_RATE = 30
SAMPLE_RATE = 44100
AUDIO_CHANNELS = 2
