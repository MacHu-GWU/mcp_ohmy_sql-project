# -*- coding: utf-8 -*-

"""
Singleton instance of Adapter for MCP OhMySQL.
"""

from ..config.init import config
from .adapter import Adapter

adapter = Adapter(config=config)
