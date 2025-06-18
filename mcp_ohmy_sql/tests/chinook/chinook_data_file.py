# -*- coding: utf-8 -*-

"""
In this project, we use the Chinook database as a sample database for testing.

This script automates the download of the Chinook database files from GitHub.

See: https://github.com/lerocha/chinook-database
"""

import requests

from ...paths import dir_tmp
from ...logger import logger

TAG = "v1.4.5"


def get_url(file: str, tag: str = TAG) -> str:
    """
    Get the URL for the Chinook release file based on the tag and file name.
    """
    return f"https://github.com/lerocha/chinook-database/releases/download/{tag}/{file}"


def download_file(file: str, tag: str = TAG):
    url = get_url(file, tag)
    path = dir_tmp / file
    logger.info(f"Downloading chinook file from {url} to {path} ...")
    if path.exists():
        logger.info(f"Already exists, skipping download.")
    else:
        res = requests.get(url)
        path.write_bytes(res.content)
        logger.info("Done.")


path_ChinookData_json = dir_tmp / "ChinookData.json"
path_Chinook_Sqlite_sqlite = dir_tmp / "Chinook_Sqlite.sqlite"
with logger.disabled(
    # disable=False, # show log
    disable=True,  # no log
):
    download_file("ChinookData.json")
