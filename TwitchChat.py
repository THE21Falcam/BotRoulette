# gemma3:270m
# 32k context window

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

template = """
You are a Twitch Streamer You are answring your userchat Below.

Here is the chat history: {context}

UserChat : {userchat}

Response :
"""

model = OllamaLLM(model="gemma3:1b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def handle_conversation():
    context = ""
    print("wilcome")
    while True:
        user_input = input("UserChat: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"context": context, "userchat": user_input})
        print("Result: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"


if __name__ == "__main__":
    handle_conversation()
