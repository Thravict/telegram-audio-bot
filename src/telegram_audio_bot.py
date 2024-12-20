import os
import yaml
import logging
from uuid import uuid4
from telegram import Update, InlineQueryResultVoice
from telegram.ext import Application, ContextTypes, InlineQueryHandler

config_path: str = (
    os.environ.get('CONFIG_PATH') or 
    os.path.join(os.path.dirname(__file__), "../", 'telegram_audio_bot_config.yaml')
)
with open(config_path, 'r') as file:
    config_file = yaml.safe_load(file)
config = config_file.get('telegram_audio_bot', {})

api_token: str = (os.environ.get('API_TOKEN') or config.get('api_token', ''))
voice_file_list: list = config.get('voice_file_list', [])

logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    results = [
        InlineQueryResultVoice(
            id=str(uuid4()),
            voice_url=voice_file.get("file_url"),
            title=voice_file.get("display_name"),
        )
        for voice_file in voice_file_list
    ]
    await update.inline_query.answer(results)
        
def main() -> None:
    """Start the bot."""
    application = Application.builder().token(api_token).build()
    application.add_handler(InlineQueryHandler(inline_query))
    application.run_polling()
    
if __name__ == '__main__':
    main()