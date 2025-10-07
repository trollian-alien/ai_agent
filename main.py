import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print("API key present:", bool(api_key))

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")
    if len(sys.argv) < 2:
        print("Error, no prompt provided. Usage: python3 main.py your_prompt")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages
    )

    usage = response.usage_metadata
    if sys.argv[-1] == "--verbose":
        print("User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
    print(response.text)
    
    



if __name__ == "__main__":
    main()
