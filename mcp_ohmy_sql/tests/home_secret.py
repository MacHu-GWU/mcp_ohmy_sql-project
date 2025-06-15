# -*- coding: utf-8 -*-

"""
Home Secrets Management Module

This module provides a flexible and secure mechanism for loading secrets from a JSON file.
It implements a hierarchical token-based system for lazy loading of secrets with automatic
synchronization between development and runtime environments.

**Architecture Overview**

The module is built around three core concepts:

1. **Lazy Loading**: Secrets are only loaded from disk when actually accessed
2. **Token System**: Values are represented as tokens that resolve to actual values on demand
3. **Hierarchical Access**: Type-safe navigation through nested secret structures

**File Location Strategy**

The secret file is expected to be located in one of two places:

1. **Source of Truth**: ``${PROJECT_DIR}/home_secret.json``
    - Contains the master copy of secrets
    - Should NOT be committed to version control
    - Automatically copied to runtime location when present
2. **Runtime Location**: ``${HOME}/home_secret.json``
    - Used by applications at runtime
    - Automatically updated from source of truth
    - Safe location accessible from any working directory

**Key Features**

- **Lazy Loading**: Secrets are only read from disk when accessed via ``.v`` property
- **Hierarchical Navigation**: Type-safe dot-notation access to nested secret values
- **Automatic Synchronization**: Source secrets automatically copied to runtime location
- **Token-based Access**: Flexible reference system for delayed value resolution
- **Robust Error Handling**: Clear error messages for missing or malformed secrets
- **IDE Support**: Full autocomplete and type checking for secret access patterns

**Direct value access**::

    # Get a secret value immediately
    github_dev_api_key = hs.v("providers.github.accounts.my_company.users.my_admin.secrets.dev.value")

**Token-based access**::

    # Create a token for later use
    token = hs.t("providers.github.accounts.my_company.users.my_admin.secrets.dev.value")
    # Resolve the token when needed
    github_dev_api_key = token.v
"""

import typing as T
import os
import json
import textwrap
import dataclasses
from pathlib import Path
from functools import cache, cached_property

__version__ = "0.1.1"
__license__ = "MIT"
__author__ = "Sanhe Hu"


# Configuration: Secret file name used in both locations
filename = "home_secret.json"

# Source of truth: Local development secrets file
# This file contains the master copy of secrets and should NOT be committed to VCS
p_here_secret = Path(filename).absolute()

# Path to the generated enum file containing flat attribute access to all secrets
# This file is auto-generated and provides a simple dot-notation alternative to the hierarchical Secret class
p_here_enum = Path("home_secret_enum.py")

# Runtime location: Home directory secrets file
# This is where applications load secrets from during execution
p_home_secret = Path.home() / filename

# boolean flag to control whether we want to sync the source secrets file to the runtime location
IS_CI = "CI" in os.environ
if IS_CI:
    IS_SYNC = True
else:
    IS_SYNC = True


def _deep_get(
    dct: dict,
    path: str,
) -> T.Union[
    str,
    int,
    list[str],
    list[int],
    dict[str, T.Any],
]:
    """
    Retrieve a nested value from a dictionary using dot-separated path notation.

    This function enables accessing deeply nested dictionary values using a simple
    string path like "providers.github.accounts.main.admin_email".

    :param dct: The dictionary to search through
    :param path: Dot-separated path to the desired value (e.g., "key1.key2.key3")

    :raises KeyError: When any part of the path doesn't exist in the dictionary

    :return: The value found at the specified path
    """
    value = dct  # Start with the root dictionary
    parts = list()
    # Navigate through each part of the dot-separated path
    for part in path.split("."):
        parts.append(part)
        if part in value:
            value = value[part]  # Move deeper into the nested structure
        else:
            # Provide clear error message showing exactly what key was missing
            current_path = ".".join(parts)
            raise KeyError(f"Key {current_path!r} not found in the provided data.")
    return value


@dataclasses.dataclass
class Token:
    """
    A lazy-loading token that represents a reference to a secret value.

    Tokens are placeholders for values that aren't resolved when the token object
    is created. Instead, the actual secret value is loaded from the JSON file
    only when accessed via the ``.v`` property. This enables:

    - **Deferred Loading**: Values are only read from disk when actually needed
    - **Reference Flexibility**: Tokens can be passed around and stored before resolution
    - **Error Isolation**: JSON parsing errors only occur when values are accessed

    :param data: Reference to the loaded JSON data dictionary
    :param path: Dot-separated path to the secret value within the JSON structure
    """

    data: dict[str, T.Any] = dataclasses.field()
    path: str = dataclasses.field()

    @property
    def v(self):
        """
        Lazily load and return the secret value from the JSON data.

        :return: The secret value at the specified path
        """
        return _deep_get(dct=self.data, path=self.path)


@dataclasses.dataclass(frozen=True)
class HomeSecret:
    """
    Main interface for loading and accessing secrets from the home_secret.json file.

    This class provides the core functionality for the secrets management system:

    - **Automatic File Management**: Handles copying from source to runtime location
    - **Lazy Loading**: JSON is only parsed when first accessed
    - **Caching**: Parsed JSON data is cached for subsequent access
    - **Flexible Access**: Supports both direct value access and token creation
    """

    @cached_property
    def data(self) -> dict[str, T.Any]:
        """
        Load and cache the secret data from the ``home_secret.json`` file.
        """
        # Synchronization: Copy source file to runtime location if it exists
        # This allows developers to edit the local file and have changes automatically
        # propagated to the runtime environment
        if IS_SYNC:
            if p_here_secret.exists():
                p_home_secret.write_text(
                    p_here_secret.read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
        if not p_home_secret.exists():
            raise FileNotFoundError(f"Secret file not found at {p_home_secret}")
        return json.loads(p_home_secret.read_text(encoding="utf-8"))

    @cache
    def v(self, path: str):
        """
        Direct access to secret values using dot-separated path notation.

        This method provides immediate access to secret values without creating
        intermediate token objects. It's the most direct way to retrieve secrets
        when you need the value immediately.

        .. note::

            V stands for Value.
        """
        return _deep_get(dct=self.data, path=path)

    @cache
    def t(self, path: str) -> Token:
        """
        Create a Token object for deferred access to secret values.

        This method creates a token that can be stored, passed around, and resolved
        later when the actual value is needed. This is useful for:

        - **Configuration Objects**: Store tokens in config classes
        - **Dependency Injection**: Pass tokens to components that resolve them later
        - **Conditional Access**: Create tokens but only resolve them when needed

        .. note::

            T stands for Token.
        """
        return Token(
            data=self.data,
            path=path,
        )


# Global instance: Single shared secrets manager for the entire application
# This follows the singleton pattern to ensure consistent access to secrets
# across all modules that import this file
hs = HomeSecret()

UNKNOWN = "..."
DESCRIPTION = "description"
TAB = " " * 4


def walk(
    dct: dict[str, T.Any],
    _parent_path: str = "",
) -> T.Iterable[tuple[str, T.Any]]:
    """
    Recursively traverse a nested dictionary structure to extract all leaf paths and values.

    This function performs a depth-first traversal of the secrets JSON structure,
    yielding dot-separated paths to all non-dictionary values while filtering out
    metadata fields and placeholder values.

    **The traversal logic**:

    - Recursively descends into dictionary values
    - Skips 'description' fields (metadata)
    - Skips values equal to UNKNOWN ("..." placeholder)
    - Yields complete dot-separated paths for all other leaf values

    :param dct: Dictionary to traverse (typically the loaded secrets JSON)
    :param _parent_path: Current path prefix for recursive calls (internal use)

    :yields: Tuples of (path, value) where path is dot-separated and value is the leaf data

    Example::

        data = {
            "providers": {
                "github": {
                    "accounts": {
                        "main": {
                            "admin_email": "admin@example.com",
                            "description": "Main account",  # Skipped
                            "tokens": {
                                "api": {
                                    "value": "secret_token",
                                    "name": "API Token"
                                }
                            }
                        }
                    }
                }
            }
        }

        # Results in:
        # ("providers.github.accounts.main.admin_email", "admin@example.com")
        # ("providers.github.accounts.main.tokens.api.value", "secret_token")
        # ("providers.github.accounts.main.tokens.api.name", "API Token")
    """
    for key, value in dct.items():
        path = f"{_parent_path}.{key}"
        print(path, key, value)
        if isinstance(value, dict):
            if key == "value":
                yield path[1:], value
            yield from walk(
                dct=value,
                _parent_path=path,
            )
        elif key == DESCRIPTION:
            continue
        elif value == UNKNOWN:
            continue
        else:
            yield path[1:], value


def gen_enum_code():
    """
    Generate a flat enumeration class providing direct attribute access to all secrets.

    This function creates an alternative access pattern to the hierarchical Secret class
    by generating a flat class where each secret path becomes a simple attribute name.
    The generated code provides:

    - **Flat Access**: All secrets accessible as `Secret.provider__account__path`
    - **Auto-Generation**: Automatically discovers all paths in the JSON structure
    - **Validation Function**: Includes a function to test all generated paths
    - **Simple Imports**: Minimal dependencies for the generated file

    **Path Transformation Logic**:

    - Removes "providers." prefix from paths
    - Converts dots to double underscores for valid Python identifiers
    - Preserves the complete path hierarchy in the attribute name
    """
    # Build the generated file content line by line
    lines = [
        textwrap.dedent(
            """
        try:
            from home_secret import hs
        except ImportError:  # pragma: no cover
            pass
        
        
        class Secret:
            # fmt: off
        """
        )
    ]

    # Extract all secret paths from the loaded JSON data
    path_list = [path for path, _ in walk(hs.data)]

    # Generate an attribute for each discovered secret path
    for path in path_list:
        # Transform the path into a valid Python attribute name
        # Remove "providers." prefix and convert dots to double underscores
        attr_name = path.replace("providers.", "", 1).replace(".", "__")
        lines.append(f'{TAB}{attr_name} = hs.t("{path}")')

    # Add validation function and main block to the generated file
    lines.append(
        textwrap.dedent(
            """
                # fmt: on
            
            
            def _validate_secret():
                print("Validate secret:")
                for key, token in Secret.__dict__.items():
                    if key.startswith("_") is False:
                        print(f"{key} = {token.v}")
            
            
            if __name__ == "__main__":
                _validate_secret()
        """
        )
    )
    # Write the generated code to the enum file
    p_here_enum.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    gen_enum_code()

# ==============================================================================
# IDE-Friendly Usage: Copy Generated Enum
#
# After running gen_enum_code(), you can copy the entire generated Secret class
# from home_secret_enum.py and paste it below this comment block to get:
#
# 1. Full IDE autocomplete support for all secret paths
# 2. Static type checking without runtime file generation
# 3. Direct access to secrets without importing the enum file
# 4. Version control friendly - enum stays in sync with your JSON structure
#
# Simply run this file once to generate the enum, then copy-paste the
# Secret class definition here for immediate IDE integration.
# ==============================================================================
# ==============================================================================
# Home Secret Enum Class below
# ==============================================================================

try:
    from home_secret import hs
except ImportError:  # pragma: no cover
    pass


class Secret:
    # fmt: off
    db__esc_dev_mcp_ohmy_sql_dev__username = hs.t("providers.db.esc_dev_mcp_ohmy_sql_dev.username")
    db__esc_dev_mcp_ohmy_sql_dev__password = hs.t("providers.db.esc_dev_mcp_ohmy_sql_dev.password")
    # fmt: on


def _validate_secret():
    print("Validate secret:")
    for key, token in Secret.__dict__.items():
        if key.startswith("_") is False:
            print(f"{key} = {token.v}")


if __name__ == "__main__":
    _validate_secret()
