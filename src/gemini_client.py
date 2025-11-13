from google import genai
import os
from dotenv import load_dotenv

class GeminiCallback():
    
    def __init__(self):
        load_dotenv(dotenv_path="config\\.env")
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def chat_withgemini(self,prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    

def main():
    gemini = GeminiCallback()
    reply = gemini.chat_withgemini("Hello")
    print(reply)

if __name__ == "__main__":
    main()