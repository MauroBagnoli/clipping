
# Telegram Bots + Django

This Django application integrates with Telegram Bot API to allow users to send news articles to a Telegram bot. The bot then stores these articles in a database for later retrieval and analysis.

## Installation

### Create the virtualenv and activate it

```bash
> python3 -m venv ./venv
> source ./venv/bin/activate
```

### Install postgres

```bash
> brew install postgresql
```

### Install the requirements

```bash
> pip3 install -r requirements.txt
```

### Create the database

```bash
> brew services start postgresql
> createdb botdb
```

### Create user admin


```bash
> createuser -P admin
> createuser -P -s postgres
> psql -U postgres -c "ALTER USER admin WITH SUPERUSER;"
```

### Run the migrations

```bash
> python3 manage.py makemigrations
> python3 manage.py migrate
```

### Create your superuser

```bash
> python3 manage.py createsuperuser
```

### Copy .env.template and rename it to .env

### Create SECRET_KEY

```bash
> python3 manage.py shell_plus
>>> from django.core.management.utils import get_random_secret_key
>>> get_random_secret_key()
```

### Run the django backend

```bash
> python3 manage.py runserver
> http://127.0.0.1:8000/admin
```

## Authentication

### Users must be created in the admin page to be recognized by the bot by the email provided

### Install ngrok

[ngrok](https://ngrok.com/download)

### Add authtoken

```bash
> ngrok config add-authtoken <token>
```

### Create ngrok url

```bash
> ngrok http 80
```

## WEBHOOK UPDATE

### [tgbotwebhook](https://django-tgbot.readthedocs.io/en/latest/management_commands/tgbotwebhook/)

## Download Telegram for testing purposes Telegram: Contact @BotFather

### Create your API Token using BotFather

Enter this command in the command line and enter your API token:

```bash
> python3 manage.py createtgbot
Enter the bot token (retrieved from BotFather): <YOUR_TOKEN>
Setting up @BotDevTestBot ...
Enter the URL your Django project is deployed on
(if you have not deployed yet and want to test your bot, you can use services like Ngrok to do so).
```

### Set bot token

```bash
> python3 manage.py tgbottoken
```

### Check the app in INSTALLED_APPS in django's project folder

### Update the database

```bash
> python3 manage.py makemigrations
> python3 manage.py migrate
```

### Connect bot with your ngrok url

```bash
> python3 manage.py tgbotwebhook
Enter bot’s name: news_clippings_bot
Choose option 1
Paste ngrok url
Confirm (Y)
```

### Don't forget to open another terminal for Django

```bash
> python3 manage.py runserver
```

### Open Telegram and Search for @news_clippings_bot

## Django translations

### Make messages

```bash
> python3 manage.py makemessages --locale es
```

### Compile messages

```bash
> python3 manage.py compilemessages --locale es
```

## TO DROP DATABASE

```bash
> \connect postgres
```

```bash
> drop database botdb
```

```bash
> create database botdb
```
