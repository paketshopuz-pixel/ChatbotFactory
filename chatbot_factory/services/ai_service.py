# chatbot_factory/services/ai_service.py
"""
AI Service module for integrating with Google Gemini AI
"""
import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)

class AIService:
    """Service class for AI operations using Google Gemini"""
    
    def __init__(self):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.model_name = "gemini-pro"
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                logger.info("Google Gemini AI service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google Gemini: {str(e)}")
                self.model = None
        
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate AI response for a given prompt using Google Gemini
        
        Args:
            prompt: User input prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            if not self.api_key:
                logger.warning("AI API key not configured")
                return {
                    "response": "Kechirasiz, AI xizmati sozlanmagan. Iltimos, administratorga murojaat qiling.",
                    "error": "missing_api_key",
                    "success": False
                }
            
            if not self.model:
                logger.error("AI model not initialized")
                return {
                    "response": "Kechirasiz, AI modeli ishga tushmagan. Iltimos, qayta urinib ko'ring.",
                    "error": "model_not_initialized",
                    "success": False
                }
            
            # Prepare the full prompt with system context
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"Tizim ko'rsatmasi: {system_prompt}\n\nFoydalanuvchi: {prompt}"
            
            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                result = {
                    "response": response.text,
                    "model": self.model_name,
                    "success": True
                }
                logger.info(f"Generated AI response for prompt length: {len(prompt)}")
                return result
            else:
                logger.warning("Empty response from AI model")
                return {
                    "response": "Kechirasiz, AI javob bera olmadi. Iltimos, boshqa so'rov bilan urinib ko'ring.",
                    "error": "empty_response",
                    "success": False
                }
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return {
                "response": "Kechirasiz, so'rovingizni qayta ishlashda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
                "error": str(e),
                "success": False
            }
    
    def validate_api_key(self) -> bool:
        """
        Validate if AI service is properly configured
        
        Returns:
            Boolean indicating if service is ready
        """
        return bool(self.api_key and self.model)

# Global AI service instance
ai_service = AIService()
