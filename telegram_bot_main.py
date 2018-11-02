import argparse
import requests
import sys
import time
import telebot

class TelegramBot:
    def __init__(self, token, sleep_time):
        self.token = token
        self.sleep_time = sleep_time
        self.bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=["text"])
    def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
        bot.send_message(message.chat.id, message.text)

    def run(self):
        while True:
            pass
            time.sleep(self.sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--token','-T', type=str, help='Telegram Bot token', required=True)
    parser.add_argument('--sleep-time', '-S', type=str, help='Sleep time of bot between refreshes, sec', default=2)
    args = parser.parse_args()

    bot = TelegramBot(args.token, args.sleep_time)
    bot.run()


