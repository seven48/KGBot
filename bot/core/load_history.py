import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from bot.core.parser import BaseWorkspaceParser, parse_timestamp


class LoadHistory(BaseWorkspaceParser):
    """ Channels history parser. """

    def load_history(self, channel_name):
        self.switch_channel(channel_name)

        messages_list = []

        page_html = self.browser.html
        soup = BeautifulSoup(page_html, 'html.parser')

        all_messages = []
        buffer_first_message_link = None
        first_message_link = None

        while True:
            print('Scroll top')  # TODO DELETE
            self.scroll_top()

            checking_messages = soup.findAll(
                'div',
                {'class': 'c-virtual_list__item'}
            )

            # Getting first message
            for message in checking_messages:
                message_link = message.find(
                    'a',
                    {'class': 'c-timestamp--static'}
                )
                if message_link:
                    buffer_first_message_link = first_message_link
                    first_message_link = message_link
                    break

            if not first_message_link:
                continue

            if buffer_first_message_link == first_message_link:
                break

            regexp = r'.+\/\w(\d+)$'
            link = first_message_link['href']
            timestamp = re.match(regexp, link).group(1)
            timestamp = int(timestamp)
            message_datetime = parse_timestamp(timestamp)

            period = timedelta(days=30)
            minimal_datetime = datetime.now() - period

            print('Checking date')  # TODO DELETE

            if message_datetime < minimal_datetime:
                print('Found minimal date')  # TODO DELETE
                break

        all_messages = checking_messages  # TODO Find first

        current_author = 'Author'
        for message_el in all_messages:
            author = message_el.find(
                'button',
                {'class': 'c-message__rollup_member'}
            )
            if author:
                current_author = author.text

            message_text = message_el.find(
                'span',
                {'class': 'c-message__body'}
            )
            if not message_text:
                continue
            if 'c-message__body--automated' in message_text['class']:
                continue
            message_text = message_text.text

            message_url = message_el.find(
                'a',
                {'class': 'c-timestamp--static'}
            )
            message_url = message_url['href']

            regexp = r'.+\/\w(\d+)$'
            timestamp = re.match(regexp, message_url).group(1)
            timestamp = int(timestamp)
            message_datetime = parse_timestamp(timestamp)

            obj_message = {
                'author': current_author,
                'text': message_text,
                'datetime': message_datetime,
                'link': message_url
            }

            messages_list.append(obj_message)

        return messages_list
