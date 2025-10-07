import os, sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# python
print("API key present:", bool(api_key))

from google import genai

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents='Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
    )
    print(response.text)

    usage = response.usage_metadata
    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")
    
    



if __name__ == "__main__":
    main()
