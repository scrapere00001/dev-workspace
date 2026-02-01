#!/usr/bin/env python3
"""
Telegram Bot powered by Google Gemini API
"""
import os
import sys
import logging
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configurations
TELEGRAM_TOKEN = "7375590880:AAEcJ6KtpNQ69yocL1an-LtyT-bI7LULfKY"
GOOGLE_API_KEY = "AIzaSyC4HZkkrqGPNXpZzsQIz--rdcT4TcNy3ds"  # Using the selected working key

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I am a Gemini-powered bot. Send me a message and I'll reply using Google's AI models."
    )

def generate_gemini_response(text):
    """Generate response using Google Gemini API directly via requests"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": text}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            return "I couldn't generate a response (No candidates)."
        elif response.status_code == 429:
            return "⚠️ I'm currently rate limited (Quota Exceeded). Please try again later."
        else:
            return f"Error: Google API returned status {response.status_code}"
            
    except Exception as e:
        return f"Error generating response: {str(e)}"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message using Gemini."""
    user_message = update.message.text
    
    # Notify user we are thinking
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Get response from Gemini
    response_text = generate_gemini_response(user_message)
    
    # Send response
    await update.message.reply_text(response_text)

def main() -> None:
    """Start the bot."""
    print("Starting Telegram Bot...")
    print(f"Bot Username: @KimNetworkEventUser_bot")
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
