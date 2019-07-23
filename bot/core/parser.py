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
from urllib.parse import urljoin

from splinter import Browser

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
                 page_load_timeout=30, sticky_timeout=30):
        self._base_addr = base_addr
        self.browser = Browser(browser, headless=False, wait_time=30,
                               executable_path=executable_path)
        self.browser.driver.implicitly_wait(sticky_timeout)
        self.browser.driver.set_page_load_timeout(page_load_timeout)
        self.browser.driver.set_window_size(*browser_window_size)
        self.browser.visit(self._base_addr)

    def __del__(self):
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
        url = urljoin(
            self.workspace.url,
            '/messages/{0}'.format(channel_name)
        )
        self.browser.visit(url)

    def scroll_top(self):
        """ Scroll messages container to top. """
        js_script = """document
            .querySelector('div.c-message_list div.c-scrollbar__hider')
            .scrollTop = 0"""
        self.browser.execute_script(js_script)
