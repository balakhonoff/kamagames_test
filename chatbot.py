import argparse
import telebot
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', '-T', type=str, help='Telegram Bot token', required=True)
    parser.add_argument('--debug', action='store_true', help='Fulfilled list of names')
    args = parser.parse_args()

    # Хранение состояний чат-бота для разных чатов
    states = {}

    # Тестовые данные
    if args.debug:
        info = {
            35: ['Иванов', '23', 'мужской', 'Москва', 'РФ'],
            23: ['Петров', '42', 'мужской', 'Киев', 'Украина'],
            53: ['Сидоров', '12', 'мужской', 'Минск', 'Белоруссия'],
            33: ['Иванова', '33', 'женский', 'Вашингтон', 'США'],
            34: ['Петрова', '25', 'женский', 'Сидней', 'Австралия']
        }
    # Пустой словарь
    else:
        info = {}

    bot = telebot.TeleBot(args.token)

    # Поиск - логарифмическая сложность
    def search_binary(id_sorted_list, id):
        low = 0
        up = len(id_sorted_list)
        while low != up:
            cur_index = (low + up) // 2  # Целочисленный тип в Python имеет неограниченную длину
            if id == id_sorted_list[cur_index]:
                return cur_index
            elif id < id_sorted_list[cur_index]:
                up = cur_index
            else:
                low = cur_index + 1
        return None

    # Сортировка вставками
    def insertion_sort(id_not_sorted_list):
        a = id_not_sorted_list.copy()
        for i in range(len(a)):
            v = a[i]
            j = i
            while (a[j - 1] > v) and (j > 0):
                a[j] = a[j - 1]
                j = j - 1
            a[j] = v

        return a

    # Команда старт
    @bot.message_handler(commands=["start"])
    def create_new(message):
        bot.send_message(message.chat.id, 'Введите через запятую: ФИО, возраст, пол, город, страну')
        states[message.chat.id] = 1

    # Команда список
    @bot.message_handler(commands=["list"])
    def show_all(message):
        if len(info) > 0:
            list_ids = list(info.keys())
            for id in insertion_sort(list_ids):
                bot.send_message(message.chat.id, 'ID {} - '.format(id) + ', '.join(info[id]))
        else:
            bot.send_message(message.chat.id, 'Список пуст, создайте новую запись, используя команду /start')

    # Команда удаление
    @bot.message_handler(commands=["del"])
    def delete_by_id(message):
        bot.send_message(message.chat.id, 'Введите ID записи для удаления')
        states[message.chat.id] = 2

    # Произвольный текст и прием ответа после вопроса
    @bot.message_handler(content_types=['text'])
    def get_answers(message):
        if message.chat.id not in states.keys():
            states[message.chat.id] = 0
        if states[message.chat.id] == 0:
            bot.send_message(message.chat.id,
                             'Доступные команды:\n'
                             '/start - создать новую запись о человеке\n'
                             '/list - просмотреть список людей\n'
                             '/del - удалить запись о человеке из списка')
        # Прием ответа после запроса на ввод
        elif states[message.chat.id] == 1:
            parsed = message.text.strip().split(',')
            if len(parsed) != 5:
                bot.send_message(message.chat.id, 'Проверьте количество полей и введите еще раз: '
                                                  'имя, возраст, пол, город, страну')
            else:
                for i in range(5):
                    parsed[i] = parsed[i].strip()
                    if len(parsed[i]) == 0:
                        bot.send_message(message.chat.id, 'Одно из полей отсутствует, введите еще раз')
                        return
                try:
                    parsed[1] = int(parsed[1])
                    if parsed[1] < 0:
                        bot.send_message(message.chat.id,
                                         'Возраст не может быть отрицательным, введите еще раз')
                        return
                    parsed[1] = str(parsed[1])

                except:
                    bot.send_message(message.chat.id, 'Проверьте, что поле возраст - целое положительное число, введите еще раз')
                    return

                if parsed[2].lower() not in ['мужской', 'женский']:
                    bot.send_message(message.chat.id,
                             'Проверьте, что поле пол соотвествует одному из вариантов: 1) мужской, 2) женский')
                    return

                while True:
                    index = random.randint(1, 1000000)
                    if index not in info.keys():
                        info[index] = parsed
                        break
                states[message.chat.id] = 0

                bot.send_message(message.chat.id, 'Запись успешно добавлена')
        # Прием ответа после запроса на удаление
        elif states[message.chat.id] == 2:
            try:
                id_to_del = int(message.text.strip())
            except Exception:
                bot.send_message(message.chat.id, 'Ошибка, ID - целое положительное число?')
                return
            if id_to_del <= 0:
                bot.send_message(message.chat.id, 'Запись отсутствует')
            else:
                keys = insertion_sort(list(info.keys()))
                index = search_binary(keys, id_to_del)
                if index is not None:
                    del info[keys[index]]
                    bot.send_message(message.chat.id, 'Запись успешно удалена')
                else:
                    bot.send_message(message.chat.id, 'Запись отсутствует')

    bot.polling(none_stop=True)