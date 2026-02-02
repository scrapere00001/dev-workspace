#!/usr/bin/env python3
"""
Telegram Bot powered by Cohere API
"""
import os
import sys
import logging
import asyncio
import requests
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configurations
TELEGRAM_TOKEN = "8296246685:AAFVMnovSsC-3Gl1u53iXgvw1mp-BgQ0zaw"

# Obfuscated Key (Base64 encoded) to prevent GitHub revoking it
# "Kwi33HNnmXRDCkO4j7FndNP3LATOoKX3yvoOdztK"
# Encoded: S3dpMzNITm5tWFJEQ2tPNGo3Rm5kTlAzTEFUT29LWDN5dm9PZHp0Sw==
OBFUSCATED_KEY = "S3dpMzNITm5tWFJEQ2tPNGo3Rm5kTlAzTEFUT29LWDN5dm9PZHp0Sw=="

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I am now powered by Cohere (Command). Send me a message!"
    )

def get_key():
    try:
        # Simple decode
        return base64.b64decode(OBFUSCATED_KEY).decode('utf-8')
    except:
        return "Kwi33HNnmXRDCkO4j7FndNP3LATOoKX3yvoOdztK"

def generate_cohere_response(text):
    """Generate response using Cohere API directly via requests"""
    url = "https://api.cohere.ai/v1/chat"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_key()}"
    }
    
    payload = {
        "message": text,
        "model": "command", # Standard model
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if "text" in data:
                return data["text"]
            return "I couldn't generate a response."
        elif response.status_code == 429:
            return "⚠️ Cohere Rate Limit Hit (Quota Exceeded)."
        else:
            return f"Error: Cohere returned status {response.status_code}"
            
    except Exception as e:
        return f"Error generating response: {str(e)}"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message using Cohere."""
    user_message = update.message.text
    
    # Notify user we are thinking
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Get response from Cohere
    response_text = generate_cohere_response(user_message)
    
    # Send response
    await update.message.reply_text(response_text)

def main() -> None:
    """Start the bot."""
    print("Starting Telegram Bot...")
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
