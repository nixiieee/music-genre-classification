import telebot
import logging
from inference import predict_file
import os

with open('TOKEN.txt', 'r') as file:
    API_TOKEN = file.readline().strip()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '👋 Welcome! Please send me an audio file (WAV, or MP3) and I will process it for you.')

@bot.message_handler(content_types=['document', 'audio'])
def handle_file(message):
    sent_message = bot.reply_to(message, "⏳ Processing your file...")

    if message.content_type == 'document':
        file_extension = os.path.splitext(message.document.file_name)[-1][1:].lower()
        file_info = bot.get_file(message.document.file_id)
        src = 'files/' + message.document.file_name
    if message.content_type == 'audio':
        file_extension = os.path.splitext(message.audio.file_name)[-1][1:].lower()
        file_info = bot.get_file(message.audio.file_id)
        src = 'files/' + message.audio.file_name
    if file_extension in ['ogg', 'wav', 'mp3']:
        downloaded_file = bot.download_file(file_info.file_path)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        if os.path.exists(src):
            print(f"File {src} saved successfully.")
        else:
            print(f"File {src} cannot be found.")
            os._exit(0)

        prediction = predict_file(src)

        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text=f"🎉 Prediction: {prediction}")
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id, text="🚫 Only audio files (WAV, or MP3) are supported.")


if __name__ == '__main__':
    bot.polling()
