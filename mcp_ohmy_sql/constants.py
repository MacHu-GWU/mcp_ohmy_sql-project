# -*- coding: utf-8 -*-

import os
from pydantic import BaseModel, Field


class EnvVar(BaseModel):
    name: str = Field()
    default: str = Field(default="")

    @property
    def value(self) -> str:
        return os.environ.get(self.name, self.default)


class EnvVarNameEnum:
    FINAL_SQL_MCP_CONFIG = EnvVar(name="FINAL_SQL_MCP_CONFIG")
