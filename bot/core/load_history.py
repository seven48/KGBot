from datetime import datetime

from bs4 import BeautifulSoup

from bot.core.parser import BaseWorkspaceParser


class LoadHistory(BaseWorkspaceParser):
    """ Channels history parser. """

    def load_history(self, channel_name):
        self.switch_channel(channel_name)

        messages_list = []

        page_html = self.browser.html
        soup = BeautifulSoup(page_html, 'html.parser')

        all_messages = soup.findAll('div', {'class': 'c-virtual_list__item'})
        all_messages.reverse()

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

            # TODO PARSING DATETIME STRING
            message_datetime = datetime.now()

            message_url = message_el.find(
                'a',
                {'class': 'c-timestamp--static'}
            )
            message_url = message_url['href']

            obj_message = {
                'author': current_author,
                'text': message_text,
                'datetime': message_datetime,
                'link': message_url
            }

            messages_list.append(obj_message)

        return messages_list
