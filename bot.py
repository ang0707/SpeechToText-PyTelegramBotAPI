import telebot
import speech_recognition as sr
from pydub import AudioSegment
import os

TOKEN = "ЗДЕСЬ_ДОЛЖЕН_БЫТЬ_ВАШ_ТОКЕН_ИЗ_BOTFATHER"

bot = telebot.TeleBot(TOKEN)
r = sr.Recognizer()

def convert_ogg_to_wav(ogg_path, wav_path):
    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format="wav")

def recognize(audio_path):
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='ru-RU')
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь"
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания: {e}"

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        ogg_path = 'voice_message.ogg'
        wav_path = 'voice_message.wav'
        
        with open(ogg_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        convert_ogg_to_wav(ogg_path, wav_path)

        text = recognize(wav_path)

        bot.reply_to(message, text)

        os.remove(ogg_path)
        os.remove(wav_path)
        
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    bot.polling(non_stop=True)
