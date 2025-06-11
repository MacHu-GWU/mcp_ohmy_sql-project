
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


👀 Overview
------------------------------------------------------------------------------
``mcp_ohmy_sql`` is a powerful SQL `Model Context Protocol (MCP) <https://modelcontextprotocol.io/>`_ server that bridges AI assistants with your databases. Built on `SQLAlchemy <http://sqlalchemy.org/>`_'s robust foundation, it provides universal database connectivity with intelligent query optimization, configurable access controls, and built-in safeguards against excessive data loads to LLMs.

Transform your database interactions with natural language queries, automatic schema discovery, and intelligent result formatting—all while maintaining enterprise-grade security and performance.

See `📚 Full Documentation HERE <https://mcp-ohmy-sql.readthedocs.io/en/latest/>`_


🚀 Feature Highlights
------------------------------------------------------------------------------
**Universal Database Support**

Connect to virtually any SQL database through SQLAlchemy's proven architecture. From lightweight SQLite to enterprise PostgreSQL, MySQL, Oracle, and SQL Server—all supported out of the box.

**Multi-Database Architecture**
    Manage multiple databases and schemas simultaneously from a single MCP server. Perfect for complex environments with dev/staging/production databases or multi-tenant applications.

**Intelligent Query Optimization**
    Built-in query analysis engine prevents expensive operations, automatically limits result sets, and provides performance feedback to help you write efficient queries.

**AI-Optimized Schema Encoding**
    Schema information is compressed by ~70% using a specialized encoding format, dramatically reducing token usage while preserving all essential metadata for accurate query generation.

**Enterprise-Ready Security**
    Fine-grained table filtering, parameterized query support, and read-only operations by default. Access controls ensure your production data stays safe.


💎 Why Choose ``mcp_ohmy_sql``?
------------------------------------------------------------------------------
While other SQL MCP servers exist, ``mcp_ohmy_sql`` stands out through:

✨ **Comprehensive Database Ecosystem**
    Beyond traditional SQL databases, we're expanding to support modern data platforms including AWS Aurora, Redshift, Glue Catalog, MongoDB Atlas SQL, ElasticSearch, OpenSearch, DuckDB, and S3 data files.

🔧 **Production-Ready Architecture**
    Designed for real-world usage with connection pooling, error handling, query timeouts, and result size limits that prevent your LLM conversations from breaking.

📊 **Intelligent Result Formatting**
    Query results are automatically formatted as Markdown tables—the optimal format for LLM comprehension, using 24% fewer tokens than JSON while maintaining perfect readability.

🔒 **Security-First Approach**
    Built-in safeguards include SQL injection prevention, read-only operations, table filtering, and upcoming fine-grained access controls for enterprise deployments.

🎯 **Developer Experience**
    Comprehensive documentation, clear error messages, and extensive configuration options make setup and maintenance straightforward.

**Coming Soon**: Remote MCP server deployment, advanced access controls, and expanded database ecosystem support.

See our `ROADMAP.md <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/ROADMAP.md>`_ for the complete vision and upcoming features.


🚀️ Supported Features
------------------------------------------------------------------------------
See our `ROADMAP.md <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/ROADMAP.md>`_ for the complete vision and upcoming features.

.. list-table:: Feature Support Status
   :header-rows: 1
   :widths: 25 15 40

   * - **Feature**
     - **Status**
     - **Note**
   * - Multi Database Support
     - ✅ Supported
     -
   * - Local MCP Server via UV
     - ✅ Supported
     -
   * - Local MCP Server via Docker
     - ⏳ In Progress
     -
   * - Remote MCP Server
     - ⏳ In Progress
     -
   * - One Click to Deploy Remote MCP Server
     - ⏳ In Progress
     -
   * - Export Results to Local Files
     - ⏳ In Progress
     -
   * - Local Data File Analysis
     - ⏳ In Progress
     -
   * - User Management
     - ⏳ In Progress
     - Remote MCP server only feature
   * - Access Control Management
     - ⏳ In Progress
     - Remote MCP server only feature


🛢️ Supported Databases
------------------------------------------------------------------------------
See our `ROADMAP.md <https://github.com/MacHu-GWU/mcp_ohmy_sql-project/blob/main/ROADMAP.md>`_ for the complete vision and upcoming features.

.. list-table:: Database Support Status
   :header-rows: 1
   :widths: 25 15 40

   * - **Database**
     - **Status**
     - **Note**
   * - Sqlite
     - ✅ Supported
     - via Sqlalchemy
   * - Postgres
     - ✅ Supported
     - via Sqlalchemy
   * - MySQL
     - ✅ Supported
     - via Sqlalchemy
   * - Oracle
     - ✅ Supported
     - via Sqlalchemy
   * - MSSQL
     - ✅ Supported
     - via Sqlalchemy
   * - AWS Aurora
     - ⏳ In Progress
     - via boto3
   * - AWS Redshift
     - ⏳ In Progress
     - via boto3
   * - AWS Glue Catalog Databases
     - ⏳ In Progress
     - via boto3
   * - MongoDB
     - ⏳ In Progress
     - via Atlas SQL
   * - ElasticSearch
     - ⏳ In Progress
     - via ElasticSearch SQL
   * - OpenSearch
     - ⏳ In Progress
     - via OpenSearch SQL
   * - DuckDB
     - ⏳ In Progress
     - via duckdb
   * - Data Files on AWS S3
     - ⏳ In Progress
     - via boto3


🎯 Get Started
------------------------------------------------------------------------------
- `Quick Start Guide <https://mcp-ohmy-sql.readthedocs.io/en/latest/01-Quick-Start/index.html>`_: Set up and run the server in under 5 minutes
