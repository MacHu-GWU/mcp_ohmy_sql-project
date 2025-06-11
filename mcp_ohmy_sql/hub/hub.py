# -*- coding: utf-8 -*-

"""

"""

import typing as T
from pydantic import BaseModel, Field


from ..config.config_define import Config

from .sa_hub import SaHubMixin
from .tool_hub import ToolHubMixin

class Hub(
    BaseModel,
    SaHubMixin,
    ToolHubMixin,
):
    config: Config = Field()
