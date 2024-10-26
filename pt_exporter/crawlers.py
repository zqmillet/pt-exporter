from typing import Dict
from typing import Type
from typing import Optional
from importlib import import_module
from logging import Logger
from logging import getLogger

from crawlers import Crawler
from crawlers import User

from .configuration import load_configuration
from .configuration import Configuration

class Crawlers:
    def __init__(self, configuration_file_path: str, logger: Optional[Logger] = None):
        self.configuration: Configuration = load_configuration(configuration_file_path)
        crawlers_module = import_module('crawlers')
        self.crawlers: Dict[str, Crawler] = {}
        self.logger = logger or getLogger('dummy')

        for crawler_configuration in self.configuration.crawler_configurations:
            Class: Type[Crawler] = getattr(crawlers_module, crawler_configuration.clazz) # pylint: disable=invalid-name

            self.crawlers[crawler_configuration.clazz] = Class(
                headers=crawler_configuration.headers,
                base_url=crawler_configuration.base_url,
                proxy=crawler_configuration.proxy,
                timeout=crawler_configuration.timeout
            )

    def get_users(self) -> Dict[str, User]:
        users: Dict[str, User] = {}
        for name, crawler in self.crawlers.items():
            try:
                user = crawler.get_user()
            except Exception as exception: # pylint: disable=broad-exception-caught
                self.logger.exception(exception)
            else:
                users[name] = user
                self.logger.info(f'get user from {name} successfully') # pylint: disable=logging-fstring-interpolation
        return users
