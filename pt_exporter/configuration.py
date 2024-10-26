from typing import List
from typing import Optional

from yaml import safe_load

from pydantic import BaseModel
from pydantic import Field

class CrawlerConfiguration(BaseModel):
    header_file_path: str = Field(alias='header-file-path')
    clazz: str = Field(alias='class')
    proxy: Optional[str] = Field(default=None)
    base_url: str = Field(default='')
    timeout: Optional[float] = Field(default=None)

    @property
    def headers(self):
        headers = {}
        with open(self.header_file_path, 'r', encoding='utf8') as file:
            for line in file:
                key, value = line.strip().split(': ')
                headers[key] = value.strip()
        return headers

class Configuration(BaseModel):
    crawler_configurations: List[CrawlerConfiguration] = Field(alias='crawlers')

def load_configuration(configuration_file_path) -> Configuration:
    with open(configuration_file_path, 'r', encoding='utf8') as file:
        return Configuration.model_validate(safe_load(file))
