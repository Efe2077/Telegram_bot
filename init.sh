#!/bin/bash

# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем необходимые пакеты
sudo apt install -y python3 python3-pip python3-venv git nginx

# Настраиваем брандмауэр (если нужно)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Клонируем репозиторий (замените на свой)
git clone https://github.com/ваш-username/ваш-репозиторий.git /var/www/telegram-bot

# Создаем виртуальное окружение
python3 -m venv /var/www/telegram-bot/venv
source /var/www/telegram-bot/venv/bin/activate

# Устанавливаем зависимости
pip install -r /var/www/telegram-bot/requirements.txt

# Создаем .env файл с токенами
echo "BOT_TOKEN=ваш_токен_бота" > /var/www/telegram-bot/.env
echo "YANDEX_DISK_TOKEN=ваш_токен_яндекс_диска" >> /var/www/telegram-bot/.env

# Создаем сервис для бота
sudo bash -c 'cat > /etc/systemd/system/telegram-bot.service <<EOF
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/telegram-bot
EnvironmentFile=/var/www/telegram-bot/.env
ExecStart=/var/www/telegram-bot/venv/bin/python3 /var/www/telegram-bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

# Запускаем сервис
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Настраиваем вебхук для GitHub (если нужно)
mkdir -p /var/www/webhooks
sudo bash -c 'cat > /var/www/webhooks/telegram-bot-webhook.sh <<EOF
#!/bin/bash
cd /var/www/telegram-bot
git pull origin main
sudo systemctl restart telegram-bot
EOF'

chmod +x /var/www/webhooks/telegram-bot-webhook.sh