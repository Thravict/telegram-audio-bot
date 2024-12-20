import os
from html import escape
from uuid import uuid4
from handlers.logger_handler import logger_handler
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedVoice, Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

# @TODO DELETE API KEY
API_KEY: str = ""
CHOSEN_FILES_PATH: str = ''
CUSTOM_USER_ID: int = 0

# Logging
logger_handler()

def get_all_local_voice_files(file_path: str) -> list[str]:
    directory: str = os.fsencode(file_path)
    voice_file_names: list[str] = [
        os.fsdecode(file_name) for file_name in os.listdir(directory)
        if os.fsdecode(file_name).endswith(".wav")
    ]
    return voice_file_names

async def upload_voice_files(context: ContextTypes.DEFAULT_TYPE, user_id: int, voice_files_path: str) -> list[dict[str, str]]:
    """Upload voice files and get their file IDs."""
    voice_file_names = get_all_local_voice_files(voice_files_path)
    uploaded_files = []
    for voice_file_name in voice_file_names:
        with open(f"{voice_files_path}/{voice_file_name}", 'rb') as voice_file:
            voice_message_response = await context.bot.send_voice(chat_id=user_id, voice=voice_file, caption=voice_file_name, disable_notification=True)
            uploaded_files.append({
                "voice_file_id": voice_message_response.voice.file_id,
                "voice_file_name": voice_file_name
            })
    
    return uploaded_files

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE, voice_file_path: str, user_id: int | str) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    if not query:
        return

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Upload the voice files and get their file IDs
            file_upload_data: list[dict[str, str]] = await upload_voice_files(context, user_id, voice_file_path)
            results = [
                InlineQueryResultCachedVoice(
                    id=str(uuid4()),
                    voice_file_id=file_data["voice_file_id"],
                    title=file_data["voice_file_name"],
                )
                for file_data in file_upload_data
            ]
            await update.inline_query.answer(results)
            break  # Exit the loop if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                await update.inline_query.answer([], switch_pm_text="Failed to upload files, please try again later.", switch_pm_parameter="start")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(API_KEY).build()
    application.add_handler(InlineQueryHandler(lambda update, context: inline_query(update, context, voice_file_path=CHOSEN_FILES_PATH, user_id=CUSTOM_USER_ID)))

    application.run_polling()
    
if __name__ == '__main__':
    main()