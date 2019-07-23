from bot.core.parser import BaseWorkspaceParser
from bs4 import BeautifulSoup
from datetime import datetime


class LastMessagesParser(BaseWorkspaceParser):
    """Class for parsing last messages in workspace channels. """
    def __init__(self, messages_count, *args, **kwargs):
        self.messages_count = messages_count
        self._soup = BeautifulSoup()
        super().__init__(*args, **kwargs)

    def reload_source(self):
        html_source = self.browser.driver.execute_script(
            "return document.documentElement.outerHTML;")
        self._soup = BeautifulSoup(html_source, 'html.parser')

    def get_messages(self, channel_name):
        self.switch_channel(channel_name)
        self.reload_source()
        last_messages = self._soup.find_all('div', class_='c-message')
        author = "Author"
        for message in last_messages:
            try:
                link = message.find_all("a",
                                        class_="c-timestamp")[0].attrs["href"]
            except (AttributeError, IndexError):
                continue
            if not self.Message.objects.get(link=link):
                self.Message(author=author, link=link, text=message.text,
                             datetime=datetime.now()).save()
