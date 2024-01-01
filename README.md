# Trellobot

Trellobot - это телеграм бот для отслеживания изменений на Trello доске.

## Отображаемые действия с карточками
![functions_ru](images/functions_ru.png)
- Создание
- Изменение статуса
- Переименование
- Удаление
- Изменение описания
- Новый комментарий
- Добавление вложения
- Изменение даты дедлайна

## Конфигурация
Все изменения конфигурации должны производиться в config.py.
Шаблон можно найти в файле [config.py.example](https://github.com/AivenGog/trellobot/blob/master/config.py.example "config.py.example")
### Переменные power-up на Trello
- На [странице создания](https://trello.com/power-ups/admin/new) power-up в графе *Iframe connector* введите:
    > https://glitch.com/edit/#!/trello-power-up-skeleton

    Заполните другие поля, выберите Workspace вашей доски.

- Сгенерируйте API ключ во вкладке API key вашего power-up

- Запишите TRELLO_API_KEY и перейдите по ссылке Token, откуда получите TRELLO_TOKEN.
    ![изображение](images/api_and_token.png)

### Получение других переменных

- Получите TELEGRAM_BOT_TOKEN у [@BotFather](t.me/BotFather)
- Для получения TRELLO_BOARD_ID скопируйте короткий код из ссылки на вашу доску
    ![изображение](images/board_id.png)
- Получите СHAT_ID группы, куда будут присылаться сообщения с помощью неофициальных клиентов телеграм или добавьте бота в группу, напишите любую /комманду и возьмите значение ["message"]["chat"]["id"] из JSON полученного из запроса к https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates . ID должен быть отрицательным целым числом.
- Укажите в WEBHOOK_URL и PORT адрес и порт сервера, который будет принимать запросы от вебхука. Не забудьте открыть порт в файрволе и сделать их видимыми в глобальной сети.

### Создание вебхука
После того, как вы заполнили все переменные в config.py и открыли доступ к машине извне, вам предстоит создать вебхук на Trello.

Сперва запустите trellobot.py и оставьте его работать, затем ЕДИНОЖДЫ в отдельном терминале запустите webhook_generate.py. В случае успеха, создастся файл webhook_json.log и в терминале выведется соответствующее сообщение.

## Запуск
Скачайте репозиторий
```bash
git clone https://github.com/AivenGog/trellobot.git && cd trellobot
```

Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate 
```

Установите необходимые библиотеки и их зависимости

```bash
pip install -r requirements.txt
```

Внесите все необходимые данные в config.py и запустите trellobot.py

```bash
python trellobot.py
```
Если программа работает и реагирует на изменения на доске без ошибок, то вы можете запустить её в фоне.

```bash
chmod +x trellobot.py
nohup trellobot.py &
```
## License

[Unlicense](https://choosealicense.com/licenses/unlicense/#/)
