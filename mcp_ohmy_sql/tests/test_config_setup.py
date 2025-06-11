# -*- coding: utf-8 -*-


import json

from ..paths import path_sample_config

from .test_config import config


def setup_test_config():
    path_sample_config.write_text(
        json.dumps(
            config.model_dump(),
            indent=4,
            ensure_ascii=False,
        ),
    )
