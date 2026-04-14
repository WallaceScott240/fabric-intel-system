import os
from groq import Groq
from dotenv import load_dotenv
from src.fabric_logic import FABRIC_KNOWLEDGE

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_fabric_recommendation(messages):
    system_prompt = {
        "role": "system", 
        "content": FABRIC_KNOWLEDGE
    }
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[system_prompt] + messages,
            temperature=0.6,
            max_tokens=3000,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq: {str(e)}"