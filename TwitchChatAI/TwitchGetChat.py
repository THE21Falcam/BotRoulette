# https://www.twitch.tv/popout/{TwitchUser}/chat?popout=
# Twitch Chat WebSocket EndPoint
# wss://irc-ws.chat.twitch.tv/
# PASS SCHMOOPIIE
# NICK justinfan30469
# JOIN #revotopia

import socket

# Configure Credentials
server = "irc.chat.twitch.tv"
port = 6667
nickname = "justinfan30469"
token = "oauth:SCHMOOPIIE"  # Default Token
channel = "#revotopia"

# Initialize Socket
sock = socket.socket()
sock.connect((server, port))

# Authenticate and Join
sock.send(f"PASS {token}\n".encode("utf-8"))
sock.send(f"NICK {nickname}\n".encode("utf-8"))
sock.send(f"JOIN {channel}\n".encode("utf-8"))

# Receive and Parse Data
while True:
    resp = sock.recv(2048).decode("utf-8")
    if resp.startswith("PING"):
        sock.send("PONG\n".encode("utf-8"))
    elif len(resp) > 0 and "justinfan30469" not in resp:
        print(resp)
        # Parse logic here for user and message
