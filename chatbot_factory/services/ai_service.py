# chatbot_factory/services/ai_service.py
import os
import logging
import google.generativeai as genai

# Bu faylda DB bilan ishlash uchun models.py ni import qilamiz
from ..models import KnowledgeBase 

class AIService:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            logging.warning("GOOGLE_API_KEY not found. AI responses will be disabled.")
            self.model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logging.info("Google Gemini AI service configured successfully.")
        except Exception as e:
            logging.error(f"Error configuring Gemini AI: {e}")
            self.model = None

    async def get_response(self, bot, user_message):
        if not self.model:
            return "Sorry, the AI service is currently unavailable."
        
        try:
            # --- BILIMLAR BAZASI INTEGRATSIYASI ---
            knowledge_context = ""
            entries = bot.knowledge_base
            if entries:
                knowledge_context += "\n\n--- MUHIM BILIMLAR BAZASI ---\n"
                for entry in entries:
                    knowledge_context += f"MAVZU: {entry.title}\nMA'LUMOT: {entry.content}\n\n"
                knowledge_context += "--- BILIMLAR BAZASI TUGADI ---\n"
                knowledge_context += "Foydalanuvchi savoliga javob berish uchun YUQORIDAGI BILIMLAR BAZASIDAN foydalaning. Agar savol bu ma'lumotlarga aloqador bo'lmasa, umumiy bilimingizdan foydalanib javob bering."

            system_instruction = f"{bot.system_prompt}\nSizning ismingiz \"{bot.name}\".\n{knowledge_context}"
            
            response = await self.model.generate_content_async(
                user_message,
                generation_config=genai.types.GenerationConfig(temperature=0.7),
                system_instruction=system_instruction
            )
            return response.text.strip()
        except Exception as e:
            logging.error(f"AI Service error during response generation: {e}")
            return "Texnik nosozliklar tufayli javob bera olmayman. Iltimos, keyinroq qayta urinib ko'ring."

# Global AI service instance
ai_service = AIService()