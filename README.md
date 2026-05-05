

Telegram bot for homework management.

This is his third version written on Aiogram

Used technologies:

-aiogram
-sqlalchemy
-pandas
-aiosqlite
-requests
-Groq 

This bot can:

-send you tsk chosen by subject
-send all tasks for tomorrow
-send you bitcoin price in usd and eur as an author's joke
-convert all your homework into a excel file
-let you ask ai for anything in gpt-dialog mode

How to run:

```bash
git clone https://github.com/weecunya/telegram-bot-for-hw.git
cd homework-bot
cp .env.example .env
docker build -t homework-bot .
docker run -d -- homework-bot


