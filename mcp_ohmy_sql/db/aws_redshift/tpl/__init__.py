# -*- coding: utf-8 -*-

import jinja2
from functools import cached_property
from pathlib import Path

dir_here = Path(__file__).absolute().parent


def load_template(name: str) -> jinja2.Template:
    path = dir_here / f"{name}.jinja"
    text = path.read_text(encoding="utf-8").strip()
    return jinja2.Template(text)


class _TemplateEnum:
    @cached_property
    def table_info(self) -> jinja2.Template:
        return load_template("table_info")

    @cached_property
    def schema_info(self) -> jinja2.Template:
        return load_template("schema_info")

    @cached_property
    def database_info(self) -> jinja2.Template:
        return load_template("database_info")


TemplateEnum = _TemplateEnum()
