# -*- coding: utf-8 -*-

"""
Optional Dependency Loader for Database-Related Libraries.

This module provides lazy import fallbacks for several commonly used third-party
libraries in AWS and database workflows, such as `sqlalchemy`, `boto3`, and
`redshift_connector`.

If a dependency is not installed, instead of immediately raising an ImportError,
this module returns a :class:`Library` proxy object that delays the error until the user
tries to access any attribute. This allows for better user experience and optional
dependency management in larger applications or libraries.

Usage:

>>> from mcp_ohmy_sql.lazy_import import sa
"""

class Library:
    def __init__(self, name: str, message: str = "please install it"):
        self.name = name
        self.message = message

    def __repr__(self):
        return f"Library({self.name})"

    def __getattr__(self, attr: str):
        raise ImportError(
            f"You didn't install `{self.name}`. To use `{attr}`, {self.message}."
        )


try:
    import sqlalchemy as sa
    import sqlalchemy.exc as sa_exc
except ImportError:  # pragma: no cover
    sa = Library("sqlalchemy")
    sa_exc = Library("sqlalchemy")

try:
    import boto3
except ImportError:  # pragma: no cover
    boto3 = Library("boto3")

try:
    from boto_session_manager import BotoSesManager
except ImportError:  # pragma: no cover
    BotoSesManager = Library("boto_session_manager")

try:
    import redshift_connector
except ImportError:  # pragma: no cover
    redshift_connector = Library("redshift_connector")

try:
    import simple_aws_redshift.api as aws_rs
except ImportError:  # pragma: no cover
    aws_rs = Library("simple_aws_redshift")
