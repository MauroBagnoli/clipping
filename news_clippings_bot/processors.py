import os
from dotenv import load_dotenv

from django.utils.translation import gettext as _
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from .utils import (
    get_urls_from_message,
    get_message_without_urls,get_author_from_message,
    get_tag_from_message,
    get_is_valid_email,
)

from apps.users.models import User
from apps.clipping.models import Clipping

load_dotenv()

STATES = {
    'USER_IS_AUTHENTICATED': 'USER_IS_AUTHENTICATED',
    'ASKED_FOR_EMAIL': 'ASKED_FOR_EMAIL',
}


BOT_PASSPHRASE = os.getenv('BOT_PASSPHRASE')

@processor(
    state_manager,
    fail='',
)
def handle_authentication(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        # Message
        user_id = update.get_user().get_id()
        user_message = update.get_message().get_text()

        user_is_authenticated = User.objects.filter(telegram_id=user_id).exists()

        if user_is_authenticated:
            state.set_name(STATES['USER_IS_AUTHENTICATED'])
        else:
            user_sent_passphrase = user_message == BOT_PASSPHRASE
        
            if user_sent_passphrase:
                bot.sendMessage(update.get_chat().get_id(), _('Which email are you registered with in the app?'))
                state.set_name(STATES['ASKED_FOR_EMAIL'])
            else:
                raise ProcessFailure('User is not authenticated')

    except Exception:
        print('ERROR:', Exception)


@processor(
    state_manager,
    from_states=STATES['ASKED_FOR_EMAIL'],
    fail='',
)
def validate_email(bot: TelegramBot, update: Update, state: TelegramState):
    print('validate_email')
    user_message = update.get_message().get_text()
    user_id = update.get_user().get_id()

    print('user_message: ', user_message)

    is_valid_email = get_is_valid_email(user_message)

    if not is_valid_email:
        bot.sendMessage(update.get_chat().get_id(), _('The email format is not valid. Enter the passphrase to try again.'))
        raise ProcessFailure('Invalid email address format.')

    try:
        user = User.objects.get(email=user_message)
        user.telegram_id = user_id
        user.save()

        bot.sendMessage(update.get_chat().get_id(), _('Welcome! You can now post news clippings in this chat.'))
        state.set_name(STATES['USER_IS_AUTHENTICATED'])
    except ObjectDoesNotExist:
        bot.sendMessage(update.get_chat().get_id(), _('Your email is not registered. Please contact the administrator.'))
        state.set_name('')


@processor(
    state_manager,
    success=state_types.Keep,
    from_states=STATES['USER_IS_AUTHENTICATED'],
)
def handle_clipping_entry(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        # UPDATE
        user_id = update.get_user().get_id()

        user_is_authenticated = User.objects.filter(telegram_id=user_id).exists()

        if not user_is_authenticated:
            state.set_name('')
            bot.sendMessage(update.get_chat().get_id(), _('It seems like you are not authenticated. Please contact the administrator.'))
            raise ProcessFailure('User not authenticated.')

        new_clipping = {}
        user_message = update.get_message().get_text()
        print('user_message: ', user_message)

        urls = get_urls_from_message(user_message)
        url = None

        if len(urls) > 1:
            bot.sendMessage(update.get_chat().get_id(), _('Too many URLs. I can only handle one.'))
            raise ProcessFailure('Invalid URL.')
        elif len(urls) == 1:
            url = urls[0]
            print('url: ', url)

        is_valid_url = type(url) == str
        print('is_valid_url: ', is_valid_url)


        # We know there's only one url and it's valid
        if is_valid_url:
            user_message_without_url = get_message_without_urls(user_message)
            print('user_message_without_url: ', user_message_without_url)

            new_clipping['url'] = url

            # extract autor
            if 'autor:' in user_message_without_url:
                new_clipping['author'] = get_author_from_message(user_message_without_url)
                print("new_clipping['author']", new_clipping['author'])
            
            # extract tag
            if ('tags:' or 'tag:') in user_message_without_url:
                new_clipping['tags'] = get_tag_from_message(user_message_without_url)
                print('new_clipping.tags: ', new_clipping['tags'])
            
            # TODO: GET TITLE FROM WEB HEADER

            user = User.objects.get(telegram_id=user_id)

            # Save to database
            try:
                Clipping.objects.create(
                    url=new_clipping['url'],
                    created_by=user
                )
            except IntegrityError as e:
                print(str (e))
                if 'duplicate key value violates unique constraint' in str (e):
                    bot.sendMessage(
                        update.get_chat().get_id(),
                        _('The URL of this clipping is already stored in the database.')
                    )
                    raise ProcessFailure('The URL of this clipping is already stored in the database.') 

                bot.sendMessage(
                    update.get_chat().get_id(),
                    _('There was an issue when saving the instance. Please try again or contact the administrator.')
                )
                raise ProcessFailure('An error occurred while saving the instance to the database.')

            bot.sendMessage(
                update.get_chat().get_id(),
                _('The clipping has been successfully saved in the database. Thank you!')
            )
        else:
            _('There was a problem with the provided URL. Please try again or contact the administrator.')
            raise ProcessFailure('The URL is invalid.')
    except Exception:
        print('ERROR ====> ', Exception)
