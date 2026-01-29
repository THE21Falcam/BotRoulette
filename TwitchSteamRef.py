# RTMP STREAMING
# GET https://ingest.twitch.tv/ingests
# rtmp://<ingest-server>/app/<stream-key>[?bandwidthtest=true]
# https://trac.ffmpeg.org/wiki/EncodingForStreamingSites

# Pygame Video Data To Flie
import time
from configparser import ConfigParser

import av
import numpy as np
import pygame

config = ConfigParser()
config.read("Config.ini")

WIDTH, HEIGHT = 1280, 720
FPS = 60
STREAM_KEY = config["STREAM"]["STREAM_KEY"]
TWITCH_URL = config["STREAM"]["TWITCH_URL"]
output = av.open(f"{TWITCH_URL}{STREAM_KEY}", mode="w", format="flv")

video_stream = output.add_stream("libx264", rate=FPS)
video_stream.width = WIDTH
video_stream.height = HEIGHT
video_stream.pix_fmt = "yuv420p"
video_stream.options = {
    "preset": "veryfast",
    "tune": "zerolatency",
    "profile": "baseline",
    "g": str(FPS * 2),  # keyframe every 2s
}

audio_stream = output.add_stream("aac", rate=44100)
# audio_stream.channels = 2
audio_stream.layout = "stereo"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

start_time = time.time()
audio_pts = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise KeyboardInterrupt

    screen.fill((20, 20, 30))
    pygame.draw.rect(screen, (0, 200, 255), (400, 300, 480, 120))

    # --- VIDEO ---
    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1, 0, 2))

    video_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
    video_frame = video_frame.reformat(WIDTH, HEIGHT, format="yuv420p")

    for packet in video_stream.encode(video_frame):
        output.mux(packet)

    # --- AUDIO (silent) ---
    samples = np.zeros((2, 1024), dtype=np.float32)
    audio_frame = av.AudioFrame.from_ndarray(samples, format="flt", layout="stereo")
    audio_frame.sample_rate = 44100
    audio_frame.pts = audio_pts
    audio_pts += audio_frame.samples

    for packet in audio_stream.encode(audio_frame):
        output.mux(packet)

    clock.tick(FPS)

for packet in video_stream.encode():
    output.mux(packet)

for packet in audio_stream.encode():
    output.mux(packet)

output.close()
pygame.quit()
