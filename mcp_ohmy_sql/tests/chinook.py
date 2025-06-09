# -*- coding: utf-8 -*-

import requests

from ..paths import path_chinook_sqlite


def _download_chinook_sqlite():
    """
    See: https://github.com/lerocha/chinook-database
    """
    print(f"Downloading chinook database to {path_chinook_sqlite} ...")
    url = "https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_Sqlite.sqlite"
    res = requests.get(url)
    path_chinook_sqlite.write_bytes(res.content)


def download_chinook_sqlite():
    if not path_chinook_sqlite.exists():
        _download_chinook_sqlite()


download_chinook_sqlite()
