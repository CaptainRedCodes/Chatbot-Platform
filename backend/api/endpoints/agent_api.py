

from fastapi import APIRouter
from grpc import Status
from backend.services.chatbot_service import ChatBot

router = APIRouter()


@router.post("/talk")
async def agent_chat(prompt:str):
    chat_bot = ChatBot()
    response = chat_bot.llm_chat(prompt)  
    
    return {"message": response}