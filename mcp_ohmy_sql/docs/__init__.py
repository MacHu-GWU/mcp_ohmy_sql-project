# -*- coding: utf-8 -*-

from ..paths import dir_package

doc_data = dict()

dir_docs = dir_package / "docs"


def read_file(name: str) -> str:
    return dir_docs.joinpath(name).read_text(encoding="utf-8")


class DocFiles:
    @property
    def mcp_instructions(self) -> str:
        return read_file("mcp_instructions.md")


doc_files = DocFiles()
