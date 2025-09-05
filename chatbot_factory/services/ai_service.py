# chatbot_factory/services/ai_service.py
import os
import logging
import google.generativeai as genai

class AIService:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logging.warning("GEMINI_API_KEY not found. AI responses will be disabled.")
            self.model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logging.info("Google Gemini AI service configured successfully.")
        except Exception as e:
            logging.error(f"Error configuring Gemini AI: {e}")
            self.model = None

    def generate_response(self, prompt, system_prompt, bot=None):
        """Sync method for generating response"""
        if not self.model:
            return {"response": "Kechirasiz, AI xizmati hozirda mavjud emas."}
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(temperature=0.7),
                system_instruction=system_prompt
            )
            return {"response": response.text.strip()}
        except Exception as e:
            logging.error(f"AI Service error during response generation: {e}")
            return {"response": "Texnik nosozliklar tufayli javob bera olmayman."}

    async def get_response(self, bot, user_message):
        if not self.model:
            return "Sorry, the AI service is currently unavailable."
        
        try:
            # Matnli bilimlar bazasini yig'ish
            knowledge_context = ""
            text_entries = bot.knowledge_base
            if text_entries:
                knowledge_context += "\n\n--- UMUMIY MA'LUMOTLAR BAZASI ---\n"
                for entry in text_entries:
                    knowledge_context += f"MAVZU: {entry.title}\nMA'LUMOT: {entry.content}\n\n"
            
            # Mahsulotlar bazasini yig'ish
            product_entries = bot.products
            if product_entries:
                knowledge_context += "\n\n--- MAHSULOTLAR RO'YXATI ---\n"
                for product in product_entries:
                    knowledge_context += f"MAHSULOT NOMI: {product.name}\n"
                    if product.price:
                        knowledge_context += f"NARXI: {product.price}\n"
                    if product.description:
                        knowledge_context += f"TAVSIFI: {product.description}\n"
                    if product.image_url:
                        knowledge_context += f"RASM HAVOLASI: {product.image_url}\n"
                    knowledge_context += "---\n"

            knowledge_context += "--- BILIMLAR BAZASI TUGADI ---\n"
            knowledge_context += "Foydalanuvchi savoliga javob berish uchun YUQORIDAGI BILIMLAR BAZASIDAN (Umumiy ma'lumotlar va Mahsulotlar) birinchi navbatda foydalaning. Agar savol bu ma'lumotlarga aloqador bo'lmasa, umumiy bilimingizdan foydalanib javob bering."

            system_instruction = f"{bot.system_prompt}\nSizning ismingiz \"{bot.name}\".\n{knowledge_context}"
            
            response = await self.model.generate_content_async(
                user_message,
                generation_config=genai.types.GenerationConfig(temperature=0.7),
                system_instruction=system_instruction
            )
            return response.text.strip()
        except Exception as e:
            logging.error(f"AI Service error during response generation: {e}")
            return "Texnik nosozliklar tufayli javob bera olmayman."

# Global AI service instance
ai_service = AIService()