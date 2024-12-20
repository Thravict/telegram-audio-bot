# Telegram Audio Bot

This project is a Telegram bot that allows users to send predefined audio clips via inline queries. The bot is configured using a YAML file where you can specify the API token and a list of audio files with their display names and URLs.

## Configuration

Create a configuration file named `telegram_audio_bot_config.yaml` with the following structure:

```yaml
telegram_audio_bot:
    api_token: "YOUR_API_TOKEN"
    voice_file_list:
    - display_name: "Audio Clip 1"
      file_url: "https://example.com/audio1.ogg"
    - display_name: "Audio Clip 2"
      file_url: "https://example.com/audio2.ogg"
```

### Example

Here is an example configuration:

```yaml
telegram_audio_bot:
    api_token: "0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    voice_file_list:
    - display_name: "Your File!"
      file_url: "https://your-file.ogg"
```

Replace `"YOUR_API_TOKEN"` with your actual Telegram bot API token and provide the URLs to your audio files.

## Running the Bot

To run the bot, use the following command:

```sh
poetry run telegram-audio-inline-bot
```

Make sure you have all the dependencies installed and the configuration file in place before running the bot.

## Docker Compose

You can also run the bot using Docker Compose. You can change the configuration file path and the API token as environment variables in the `docker-compose.yaml` file.

### Example `docker-compose.yaml`

```yaml
version: '3.8'

services:
  telegram-audio-bot:
    image: your-docker-image
    environment:
      - API_TOKEN=YOUR_API_TOKEN
      - CONFIG_PATH=/app/config/telegram_audio_bot_config.yaml
    volumes:
      - ./path/to/your/telegram_audio_bot_config.yaml:/app/config/telegram_audio_bot_config.yaml
```

Replace `YOUR_API_TOKEN` with your actual Telegram bot API token and provide the correct path to your configuration file.
