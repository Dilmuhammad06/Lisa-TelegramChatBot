import telebot
import google.generativeai as genai
from prompt import prompts
import json
import os

gemini_token = "" #gemini ai token
token = "" #tg bot token

genai.configure(api_key=gemini_token)
genconf = {
	"temperature":0.7,
	"top_p":0.95,
	"top_k":40,
	"max_output_tokens":150,
	"response_mime_type":"text/plain",
}


model = genai.GenerativeModel(model_name='gemini-1.5-flash',generation_config=genconf,system_instruction=prompts)

history = []

def chat(text):
    text = str(text).lower()
    chat_sessions = model.start_chat(history=history)
    result = chat_sessions.send_message(text)
    return result.text

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['lisa','liza'])
def start(message):
    bot.send_message(message.chat.id,'Lisa is here.\nTo use me add name \'Lisa\'/\'lisa\' in sentence :)')

@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_message(message.chat.id,'Support the project Lisa\n(HUMO card = \'9860 1001 2475 3847\')')

@bot.message_handler(commands=['dev'])
def dev(message):
    bot.send_message(message.chat.id,'Developer : @Dilmuhammad06')

@bot.message_handler()
def lisa(message):
    if message.chat.type in ['group','supergroup']:
        if message.reply_to_message:
            bot.reply_to(message,chat(message.text))
        elif 'Lisa' in message.text or 'lisa' in message.text or 'Liza' in message.text or 'liza' in message.text:
            bot.send_message(message.chat.id,chat(message.text))
    else:
        bot.send_message(message.chat.id,chat(message.text))
if __name__ == '__main__':
    bot.polling()
