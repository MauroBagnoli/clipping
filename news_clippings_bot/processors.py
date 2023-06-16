import os
from dotenv import load_dotenv

from django.utils.translation import gettext_lazy as _
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update

from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from .utils import get_urls_from_message, get_message_without_urls,get_author_from_message, get_tag_from_message

load_dotenv()

BOT_PASSPHRASE = os.getenv('BOT_PASSPHRASE')

# TODO: Add BOT functionality here
@processor(state_manager, from_states=state_types.All)
def handle_message(bot: TelegramBot, update: Update, state: TelegramState):
    new_clipping = {}

    try:
        # TODO: Get userIds Queryset
        authorized_user_ids = []

        # Message
        user_id = update.get_user().get_id()
        user_message = update.get_message().get_text()

        user_is_authorized = user_id in authorized_user_ids or True

        if user_is_authorized:
            urls = get_urls_from_message(user_message)
            print('urls: ', urls)
            is_valid_url = type(urls) == list and len(urls) == 1

            print('is_valid_url: ', is_valid_url)

            # We know there's only one url and it's valid
            if is_valid_url:
                user_message_without_urls = get_message_without_urls(user_message)
                print('user_message_without_urls: ', user_message_without_urls)

                new_clipping['url'] = urls[0]

                # extract autor
                if 'autor:' in user_message_without_urls:
                    new_clipping['author'] = get_author_from_message(user_message_without_urls)
                    print("new_clipping['author']", new_clipping['author'])
                
                # extract tag
                print('user_message_without_urls before tag extraction: ', user_message_without_urls)
                if ('tags:' or 'tag:') in user_message_without_urls:
                    new_clipping['tags'] = get_tag_from_message(user_message_without_urls)
                    print('new_clipping.tags: ', new_clipping['tags'])

                # happy path
                print('urls: ', urls)

                # Save to database

            else:
                # Tell the user too many urls, traducir o dejar en español.   
                bot.sendMessage(update.get_chat().get_id(), _('Too many URLs, I can handle only one'))

        else:
            user_sent_passphrase = user_message == BOT_PASSPHRASE
        
            if user_sent_passphrase:
                # Ask for email and check if valid email of existent user
                # Add user to database
                # Anser 'welcome new user!
                pass
    except Exception as ex:
        print('ERROR:', ex)

    bot.sendMessage(update.get_chat().get_id(), 'Hey Bob!')
