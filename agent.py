import os
import sys

from dotenv import load_dotenv
from anthropic import Anthropic

MODEL = "claude-sonnet-5"
SYSTEM_PROMPT = "You are a helpful, concise AI assistant."


def main():
    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    client = Anthropic(api_key=api_key)
    messages = []

    print("AI Agent ready. Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )

        reply = "".join(block.text for block in response.content if block.type == "text")
        print(f"Agent: {reply}\n")

        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
