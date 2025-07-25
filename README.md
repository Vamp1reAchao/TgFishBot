# Telegram Fish Bot

Telegram бот для работы с сессиями и автоматизации действий в Telegram с использованием aiogram и pyrogram.

## Описание

Бот предоставляет функционал для:
- Управления Telegram сессиями
- Автоматической проверки валидности сессий
- Работы с прокси
- Административной панели для управления
- Логирования действий пользователей

## Требования

- Python 3.7+
- Telegram Bot Token
- Telegram API ID и API Hash

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd "Telegram Fish Bot"
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл конфигурации `config/.env` со следующими параметрами:
```env
BOT_TOKEN=your_bot_token_here
BOT_NAME=YourBotName
BOT_VERSION=1.0
BOT_PARSE_MODE=HTML

ADMIN_ID=your_admin_id

TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

USE_PROXY=False
CHECK_VALID_SESSION=60
SPAM_IN_CONNECT_SESSION=False
SPAM_IN_RESET_AUTH=False
AUTO_CHECH_PASSWORDS=False

LOG_ENTER_START=True
LOG_ENTER_PHONE=True
LOG_GET_SESSION=True
LOG_RESET_AUTH=True
LOG_INVALID_SESSION=True

FIND_CHATS=[]
```

## Структура проекта

```
├── config/              # Конфигурационные файлы
├── images/              # Изображения для бота
├── sessions/            # Папка для сессий
├── tgbot/              # Основной код бота
│   ├── data/           # Данные и конфигурация
│   ├── dialogs/        # Диалоги пользователя
│   ├── handlers/       # Обработчики команд
│   ├── keyboards/      # Клавиатуры
│   ├── middlewares/    # Промежуточное ПО
│   ├── misc/           # Вспомогательные функции
│   ├── services/       # Сервисы
│   └── states/         # Состояния FSM
├── main.py             # Точка входа
└── requirements.txt    # Зависимости
```

## Запуск

```bash
python main.py
```

## Функционал

- `/start` - Запуск бота
- Административные команды для управления
- Работа с телефонными номерами и сессиями
- Автоматическое обновление и проверка сессий

## Отказ от ответственности

**ВНИМАНИЕ:** Автор не несет ответственности за любые действия, совершенные с использованием данного программного обеспечения. Использование бота осуществляется исключительно на ваш страх и риск. Пользователь самостоятельно несет полную ответственность за соблюдение законодательства и правил использования Telegram API.