from bot.core.parser import BaseWorkspaceParser, parse_timestamp
from bs4 import BeautifulSoup
import re
import time


class LastMessagesParser(BaseWorkspaceParser):
    """Class for parsing last messages in workspace channels. """
    def __init__(self, *args, **kwargs):
        self._soup = BeautifulSoup()
        super().__init__(*args, **kwargs)

    def reload_source(self):
        html_source = self.browser.driver.execute_script(
            "return document.documentElement.outerHTML;")
        self._soup = BeautifulSoup(html_source, 'html.parser')

    def parse_channels(self):
        all_last_messages = []
        for channel in self.workspace.channels.all():
            messages = self.get_messages(channel.name)
            all_last_messages += messages
        return all_last_messages

    def get_messages(self, channel_name, max_scrolls=50):
        self.switch_channel(channel_name)
        self.reload_source()
        author = "Author"
        curr_scroll = 0
        last_scroll = False
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

                regexp = r'.+\/\w(\d+)$'
                timestamp = re.match(regexp, link).group(1)
                timestamp = int(timestamp)
                message_datetime = parse_timestamp(timestamp)
                try:
                    self.Message.objects.get(link=link)
                except:  # noqa: E722
                    message_obj = {
                        'author': author,
                        'text': message.text,
                        'datetime': message_datetime,
                        'link': link
                    }
                    messages_list.append(message_obj)

                else:
                    last_scroll = True

            if last_scroll or (curr_scroll >= max_scrolls):
                break
            else:
                curr_scroll += 1
                self.scroll_top()
                time.sleep(2)
                self.reload_source()
        return messages_list
