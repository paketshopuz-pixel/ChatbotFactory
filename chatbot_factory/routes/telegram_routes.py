# chatbot_factory/routes/telegram_routes.py
import json
import requests
import logging
from flask import Blueprint, request, jsonify
from chatbot_factory.models import Bot
from chatbot_factory.services.ai_service import ai_service

logger = logging.getLogger(__name__)
telegram_bp = Blueprint('telegram', __name__)

@telegram_bp.route('/telegram/webhook/<bot_token>', methods=['POST'])
def telegram_webhook(bot_token):
    """Handle incoming Telegram messages"""
    try:
        # Parse incoming message
        update = request.get_json()
        
        if not update or 'message' not in update:
            return jsonify({'status': 'no message'}), 200
            
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        # Find bot by token
        bot = Bot.query.filter_by(telegram_token=bot_token).first()
        if not bot:
            logger.warning(f"Bot not found for token: {bot_token}")
            return jsonify({'status': 'bot not found'}), 404
            
        # Generate AI response
        response_data = ai_service.generate_response(
            prompt=text,
            system_prompt=bot.system_prompt
        )
        
        response_text = response_data.get('response', 'Kechirasiz, javob berish uchun xatolik yuz berdi.')
        
        # Send response back to Telegram
        send_telegram_message(bot_token, chat_id, response_text)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def send_telegram_message(bot_token, chat_id, text):
    """Send message via Telegram Bot API"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code != 200:
            logger.error(f"Failed to send telegram message: {response.text}")
        return response.json()
    except Exception as e:
        logger.error(f"Error sending telegram message: {str(e)}")
        return None

def set_telegram_webhook(bot_token, webhook_url):
    """Set webhook URL for Telegram bot"""
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    data = {'url': webhook_url}
    
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Error setting webhook: {str(e)}")
        return None

def remove_telegram_webhook(bot_token):
    """Remove webhook for Telegram bot"""
    url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    
    try:
        response = requests.post(url, timeout=10)
        return response.json()
    except Exception as e:
        logger.error(f"Error removing webhook: {str(e)}")
        return None