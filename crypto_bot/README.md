# Monad Wallet Telegram Bot

Telegram бот для взаимодействия с кошельком в сети Monad. Позволяет управлять балансом, отслеживать транзакции и получать уведомления.

📋 Функционал
- Просмотр баланса в MONAD
- История последних транзакций(в последних ста блокай блокчейна)
- Отправка токенов на другие адреса
- Уведомления о входящих платежах
- Поддержка EVM-совместимой сети Monad

⚙️ Требования
- Python 3.12+
- Аккаунт в [Telegram](https://telegram.org)
- RPC-эндпоинт сети Monad
- Приватный ключ кошелька (для тестирования используйте **только тестовый кошелек**)

🛠 Установка
1. Клонируйте репозиторий

2. Установите зависимости 
pip install -r requirements.txt

3. Создайте файл .evm
Файл должен быть следующего содержания:

BOT_TOKEN=ваш_токен_бота

MONAD_RPC_URL=https://testnet-rpc.monad.xyz

WALLET_ADDRESS=0xВашАдрес

PRIVATE_KEY=ваш_приватный_ключ

ADMIN_CHAT_ID=ваш_chat_id

4.Запустите бота - готово, удачи в отработке монада, да прибудет с вами ревард
