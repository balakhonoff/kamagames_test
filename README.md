# Тестовое задание KamaGames

Нужно написать (язык Python 3) телеграм чат бота (можно использовать готовые библиотеки реализующие интерфейс telegram api), через который можно сохранить (в памяти приложения, бд не обязательно) и запросить (о ранее сохраненном человеке) информацию.
Должны быть реализованы следующие команды:
/save - сохраняет нового человека и информацию о нем (id (инкремент, хеш от данных, что угодно), ФИО, Возраст, Пол, Город, Страна)
/list - список всех ранее сохраненных людей, отсортированных по id от меньшего к большему, сортировка должна быть реализована в коде, без использования сторонних или built-in библиотек, любой алгоритм.
/del - удаляет человека по id. Нужно сделать проверку есть ли такой человек вообще, для проверки нужно реализовать поиск по всем id, алгоритм любой быстрее O(n).

Получение, поступающих к боту команд, должно быть реализовано через метод GET из API Телеграма (т.е не через вебхуку)
Приложение должно устанавливаться как пакет c command line интерфейсом, со всеми зависимости, либо должно быть упаковано в докер.
Токен телеграмма передается внутрь через аргумент в консоли или docker run. 
Код выложить к себе на гитхаб в отдельном открытом репозитории.

# Сборка docker образа

```
$ git clone https://github.com/balakhonoff/kamagames_test.git
$ cd kamagames_test
$ docker build -t kamagames_test_chatbot .
```

# Запуск контейнера

*1. В поле <token> вписывается активный токен телеграм-бота*

*2. При запуске с флагом --debug заполняется 5 тестовых записей, 
которые можно просмотреть или удалить по одной*

```
$ docker run kamagames_test_chatbot -T <token> [--debug]
```

**Внимание: для запуска требуется VPN, либо VPS с открытым доступом к серверам Телеграма**

# Доступные команды:

*/start - создать новую запись о человеке*

*/list - просмотреть список людей*

*/del - удалить запись о человеке из списка*