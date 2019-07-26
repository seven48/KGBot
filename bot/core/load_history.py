import re
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from bot.core.parser import BaseWorkspaceParser, parse_timestamp


class LoadHistory(BaseWorkspaceParser):
    """ Channels history parser. """

    def __init__(self, *args, **kwargs):
        self._soup = BeautifulSoup()
        super().__init__(*args, **kwargs)

    def reload_source(self):
        html_source = self.browser.driver.execute_script(
            "return document.documentElement.outerHTML;")
        self._soup = BeautifulSoup(html_source, 'html.parser')

    def load_history_v2(self, channel_name, max_scrolls=8):
        self.switch_channel(channel_name)
        self.reload_source()
        author = "Author"
        curr_scroll = 0
        messages_list = []
        while True:
            last_messages = self._soup.find_all('div', class_='c-message')
            for message in last_messages:
                try:
                    link = message.find_all("a",
                                            class_="c-timestamp")[0].attrs[
                        "href"]
                except (AttributeError, IndexError):
                    continue

                author_elem = message.find(
                    'button',
                    {'class': 'c-message__rollup_member'}
                )
                if author_elem:
                    author = author_elem.text

                if link in list(map(lambda elem: elem["link"], messages_list)):
                    continue

                regexp = r'.+\/\w(\d+)$'
                timestamp = re.match(regexp, link).group(1)
                timestamp = int(timestamp)
                message_datetime = parse_timestamp(timestamp)
                message_obj = {
                    'author': author,
                    'text': message.text,
                    'datetime': message_datetime,
                    'link': link
                }
                messages_list.append(message_obj)

            if (curr_scroll >= max_scrolls) or len(messages_list) >= 300:
                break
            else:
                curr_scroll += 1
                self.scroll_top()
                time.sleep(2)
                self.reload_source()
        return messages_list
