from typing import List
from typing import Dict
from typing import Optional

from yaml import safe_load

from pydantic import BaseModel
from pydantic import Field

class CrawlerConfiguration(BaseModel):
    headers: Dict[str, str] = Field(alias='headers')
    clazz: str = Field(alias='website')
    proxy: Optional[str] = Field(default=None)
    base_url: str = Field(default='', alias='base-url')
    timeout: Optional[float] = Field(default=None)

class Configuration(BaseModel):
    crawler_configurations: List[CrawlerConfiguration] = Field(alias='crawlers')

def load_configuration(configuration_file_path) -> Configuration:
    with open(configuration_file_path, 'r', encoding='utf8') as file:
        return Configuration.model_validate(safe_load(file))
