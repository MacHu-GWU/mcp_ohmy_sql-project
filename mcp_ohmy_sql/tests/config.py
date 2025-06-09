# -*- coding: utf-8 -*-

from ..config import Config
from ..paths import path_config

config = Config.load(path_config)
chinook_db = config.databases[0]
