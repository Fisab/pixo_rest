import yaml
from typing import Optional, Union
from pixo_rest.service.exceptions import BadConfig
from pixo_rest.models.config import Config

config = None


def get_config(config_name: str = 'config.yml') -> Union[Config]:
    global config
    if config is None:
        with open(config_name, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as ex:
                raise BadConfig(f'Got error when loading config: {ex}')
    return Config(**config)
