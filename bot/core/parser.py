# Copyright 2019 Anton Maksimovich <antonio.maksimovich@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module with basic building blocks for tests. """

from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium.common.exceptions import JavascriptException
from splinter import Browser
from xvfbwrapper import Xvfb

from django.apps import apps


def parse_timestamp(timestamp):
    """ Parse datetime from timestamp with microseconds. """
    time_different = 1000000
    return datetime.fromtimestamp(timestamp / time_different)


class BaseSlackParser:
    """Class for basic slack parser functionality. """

    def __init__(self, base_addr,
                 browser="firefox",
                 executable_path="./bot/core/drivers/geckodriver",
                 browser_window_size=(1920, 1080),
                 page_load_timeout=30, sticky_timeout=30, headless=True):
        self._base_addr = base_addr
        self._headless = headless
        if self._headless:
            self.xvfb = Xvfb()
            self.xvfb.start()
        self.browser = Browser(browser, headless=False, wait_time=30,
                               executable_path=executable_path)
        self.browser.driver.implicitly_wait(sticky_timeout)
        self.browser.driver.set_page_load_timeout(page_load_timeout)
        self.browser.driver.set_window_size(*browser_window_size)
        self.browser.visit(self._base_addr)

    def __del__(self):
        if self._headless:
            self.xvfb.stop()
        self.browser.quit()


class BaseWorkspaceParser(BaseSlackParser):
    """Class for basic workspace parser functionality. """

    def __init__(self, workspace, **kwargs):
        self.workspace = workspace
        super().__init__(self.workspace.url, **kwargs)

        self.Message = apps.get_model('bot', 'Message')

        self.login(self.workspace.username, self.workspace.password)

    def login(self, username, password):
        """ Auth in Slack workspace. """
        email_field = self.browser.find_by_id('email')
        email_field.fill(username)

        password_field = self.browser.find_by_id('password')
        password_field.fill(password)

        submit_btn = self.browser.find_by_id('signin_btn')
        submit_btn.click()

    def switch_channel(self, channel_name):
        """ Switch slack channel to channel name by url visit. """
        links_list = []
        for _ in range(30):
            page_html = self.browser.html
            soup = BeautifulSoup(page_html, 'html.parser')
            links_list = soup.findAll('a', {'class': 'c-link'})
            if links_list:
                break
            sleep(1)

        for link in links_list:
            inner_span = link.find(
                'span',
                {'class': 'p-channel_sidebar__name'}
            )
            if not inner_span:
                continue

            link_name = inner_span.text
            if link_name != channel_name:
                continue

            link_href = link['href']
            self.browser.visit(link_href)

    def scroll_top(self):
        """ Scroll messages container to top. """
        js_script = """document
            .querySelector('div.c-message_list div.c-scrollbar__hider')
            .scrollTop = 0"""
        for _ in range(30):
            try:
                self.browser.execute_script(js_script)
            except JavascriptException:
                sleep(1)
            else:
                break
