
# Telegram Bots + Django

## [django-tgbot](https://github.com/Ali-Toosi/django-tgbot)

## Django Backend

### Create the virtualenv and activate it

```bash
> python3 -m venv ./venv
> source ./venv/bin/activate
```

### Install the postgres

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
> createdb marilles
```

### Create rol marilles

```bash
> createuser -P -s marilles 
```

```bash
> createuser -P marilles
> createuser -P -s postgres
> psql -U postgres -c "ALTER USER marilles WITH SUPERUSER;"
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

## WEBHOOK UPDATE

### [tgbotwebhook](https://django-tgbot.readthedocs.io/en/latest/management_commands/tgbotwebhook/)

## Download Telegram for testing purposes Telegram: Contact @BotFather

### Create your API Token using BotFather

Enter this command in the command line:

```bash
> python3 manage.py createtgbot
```

Enter your API token:

```bash
> python3 manage.py createtgbot
```

Enter the bot token (retrieved from BotFather): <YOUR_TOKEN>
Setting up @BotDevTestBot ...
Enter the URL your Django project is deployed on
(if you have not deployed yet and want to test your bot, you can use services like Ngrok to do so).

### Check the app in INSTALLED_APPS in django's project folder

### Update the database

```bash
> python3 manage.py makemigrations
> python3 manage.py migrate
```

### Install ngrok

[ngrok](https://ngrok.com/download)

### Add authtoken

```bash
> ngrok config add-authtoken <token>
```

### Create url

```bash
> ngrok http 80
```

```bash
> python3 manage.py tgbotwebhook
Enter bot’s name: news_clippings_bot
Choose option 1
Paste ngrok url
Confirm (Y)
```

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
> drop database marilles
```

```bash
> create database marilles
```
