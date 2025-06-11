#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywf import pywf

# import os
#
# path_sample_config = pywf.dir_project_root / "sample_mcp_ohmy_sql_config.json"
# os.environ["MCP_OHMY_SQL_CONFIG"] = str(path_sample_config)

pywf.build_doc(real_run=True, verbose=True)
