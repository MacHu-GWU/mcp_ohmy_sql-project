
.. image:: https://readthedocs.org/projects/mcp-ohmy-sql/badge/?version=latest
    :target: https://mcp-ohmy-sql.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/mcp_ohmy_sql-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/mcp_ohmy_sql-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/mcp_ohmy_sql-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/mcp_ohmy_sql-project

.. image:: https://img.shields.io/pypi/v/mcp-ohmy-sql.svg
    :target: https://pypi.python.org/pypi/mcp-ohmy-sql

.. image:: https://img.shields.io/pypi/l/mcp-ohmy-sql.svg
    :target: https://pypi.python.org/pypi/mcp-ohmy-sql

.. image:: https://img.shields.io/pypi/pyversions/mcp-ohmy-sql.svg
    :target: https://pypi.python.org/pypi/mcp-ohmy-sql

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/mcp_ohmy_sql-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://mcp-ohmy-sql.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/mcp_ohmy_sql-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/mcp_ohmy_sql-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/mcp_ohmy_sql-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/mcp-ohmy-sql#files


Welcome to ``mcp_ohmy_sql`` Documentation
==============================================================================
.. image:: https://mcp-ohmy-sql.readthedocs.io/en/latest/_static/mcp_ohmy_sql-logo.png
    :target: https://mcp-ohmy-sql.readthedocs.io/en/latest/

``mcp_ohmy_sql`` is a state-of-the-art SQL Model Context Protocol (MCP) server built on SQLAlchemy that provides universal database connectivity with intelligent query optimization, configurable tool exposure, and built-in safeguards against excessive data loads to LLMs. It supports schema introspection, query execution with result pagination, data export capabilities, and fine-grained access control (upcoming), making it the ideal bridge between AI assistants and SQL databases while ensuring performance, security, and flexibility across all major database engines.


.. _install:

Install
------------------------------------------------------------------------------

``mcp_ohmy_sql`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install mcp-ohmy-sql

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade mcp-ohmy-sql
