
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


👀 Overview
------------------------------------------------------------------------------
``mcp_ohmy_sql`` is a powerful SQL `Model Context Protocol (MCP) <https://modelcontextprotocol.io/>`_ server that bridges AI assistants with your databases. Built on `SQLAlchemy <http://sqlalchemy.org/>`_'s robust foundation, it provides universal database connectivity with intelligent query optimization, configurable access controls, and built-in safeguards against excessive data loads to LLMs.

Transform your database interactions with natural language queries, automatic schema discovery, and intelligent result formatting—all while maintaining enterprise-grade security and performance.

See `📚 Full Documentation HERE <https://mcp-ohmy-sql.readthedocs.io/en/latest/>`_


🚀 Key Features
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


🛢️ Supported Databases
------------------------------------------------------------------------------
.. raw:: html

    <table class="tg"><thead>
      <tr>
        <th class="tg-amwm">Database</th>
        <th class="tg-amwm">Status</th>
        <th class="tg-amwm">Note</th>
      </tr></thead>
    <tbody>
      <tr>
        <td class="tg-baqh">Sqlite</td>
        <td class="tg-baqh">✅ Supported</td>
        <td class="tg-baqh">via Sqlalchemy</td>
      </tr>
      <tr>
        <td class="tg-baqh">Postgres</td>
        <td class="tg-baqh">✅ Supported</td>
        <td class="tg-baqh">via Sqlalchemy</td>
      </tr>
      <tr>
        <td class="tg-baqh">MySQL</td>
        <td class="tg-baqh">✅ Supported</td>
        <td class="tg-baqh">via Sqlalchemy</td>
      </tr>
      <tr>
        <td class="tg-baqh">Oracle</td>
        <td class="tg-baqh">✅ Supported</td>
        <td class="tg-baqh">via Sqlalchemy</td>
      </tr>
      <tr>
        <td class="tg-baqh">MSSQL</td>
        <td class="tg-baqh">✅ Supported</td>
        <td class="tg-baqh">via Sqlalchemy</td>
      </tr>
      <tr>
        <td class="tg-baqh">AWS Aurora</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via boto3</td>
      </tr>
      <tr>
        <td class="tg-baqh">AWS Redshift</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via boto3</td>
      </tr>
      <tr>
        <td class="tg-baqh">AWS Glue Catalog Databases</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via boto3</td>
      </tr>
      <tr>
        <td class="tg-baqh">MongoDB</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via Atlas SQL</td>
      </tr>
      <tr>
        <td class="tg-baqh">ElasticSearch</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via ElasticSearch SQL</td>
      </tr>
      <tr>
        <td class="tg-baqh">OpenSearch</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via OpenSearch SQL</td>
      </tr>
      <tr>
        <td class="tg-baqh">DuckDB</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via duckdb</td>
      </tr>
      <tr>
        <td class="tg-baqh">Data Files on AWS S3</td>
        <td class="tg-baqh">⏳ In Progress</td>
        <td class="tg-baqh">via boto3</td>
      </tr>
    </tbody></table>


🎯 Get Started
------------------------------------------------------------------------------
- `Quick Start Guide <docs/source/01-Quick-Start/index.rst>`_: Set up and run the server in under 5 minutes
- `Configuration Guide <docs/source/02-Configuration/index.rst>`_: Configure multiple databases and advanced security settings
