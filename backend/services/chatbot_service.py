

from backend.core import supabase_client
from backend.core.openai_client import get_openai_client


class ChatBot:
    def __init__(self,model_name:str="allenai/molmo-2-8b:free"):
        self.model_name = model_name
        self.client = supabase_client.get_supabase_client()
        self.ai_client = get_openai_client()


    def llm_chat(self,input_text:str):
        response = self.ai_client.chat.completions.create(
            model = self.model_name,
            messages=[
                {
                "role":"user",
                "content":input_text
                }
            ]
        )

        return response.choices[0].message.content