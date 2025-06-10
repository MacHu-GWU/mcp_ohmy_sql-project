# -*- coding: utf-8 -*-

import typing as T
import re
from typing import Pattern


def match(
    name: str,
    include: list[str],
    exclude: list[str],
) -> bool:
    """
    Match a name against include and exclude lists using wildcard or regex patterns.

    The include/exclude pattern system works like a two-stage filter where name
    must pass both inclusion and exclusion criteria to be selected for processing.

    Pattern Types:

    - Wildcard patterns: Use * to match any characters (e.g., ``"EMPLOYEE*"``, ``"*_TEMP"``)
    - Regex patterns: Automatically detected when regex metacharacters are present
      (e.g., ``"^EMP.*"``, ``".*_TABLE$"``, ``"[A-Z]+_\\d+"``)

    Matching Rules:

    - Default inclusion: When include list is empty, all names are included by default
    - Include matching: When include patterns exist, a name must match ANY include
      pattern (logical OR) to be considered
    - Exclude override: If a name matches ANY exclude pattern, it's rejected
      regardless of include matches
    - Case insensitive: All pattern matching is case-insensitive

    :param name: The name to match (e.g., table name, column name)
    :param include: List of patterns to include. Empty list means include all.
    :param exclude: List of patterns to exclude. Takes precedence over include.

    Returns:
        bool: True if the name matches the criteria, False otherwise.

    Examples:
        >>> # Include all employee tables
        >>> match("EMPLOYEES", ["EMPLOYEE*"], [])
        True
        >>> match("EMPLOYEE_HISTORY", ["EMPLOYEE*"], [])
        True
        >>> match("MANAGERS", ["EMPLOYEE*"], [])
        False

        >>> # Include all, but exclude temporary tables
        >>> match("USERS", [], ["*_TEMP", "*_TMP"])
        True
        >>> match("USERS_TEMP", [], ["*_TEMP", "*_TMP"])
        False

        >>> # Include specific tables with regex
        >>> match("EMP_2023", ["^EMP_\\d{4}$"], [])
        True
        >>> match("EMP_ARCHIVE", ["^EMP_\\d{4}$"], [])
        False

        >>> # Complex filtering: include employee/manager tables, exclude history
        >>> match("EMPLOYEE_CURRENT", ["EMPLOYEE*", "MANAGER*"], ["*_HISTORY"])
        True
        >>> match("EMPLOYEE_HISTORY", ["EMPLOYEE*", "MANAGER*"], ["*_HISTORY"])
        False

        >>> # Case insensitive matching
        >>> match("employees", ["EMPLOYEES"], [])
        True
        >>> match("EMPLOYEES", ["employees"], [])
        True
    """

    # Convert wildcard patterns to regex patterns
    def pattern_to_regex(pattern: str) -> Pattern:
        # Check if pattern contains regex metacharacters (excluding *)
        # If it does, treat it as a regex pattern, otherwise treat * as wildcard
        regex_chars = r"[.+?^${}()|[\]\\]"
        has_regex = bool(re.search(regex_chars, pattern.replace("*", "")))

        if has_regex:
            # It's a regex pattern, compile as-is
            regex_pattern = pattern
        else:
            # It's a wildcard pattern, escape everything except *
            regex_pattern = re.escape(pattern)
            # Replace escaped \* with .* for wildcard matching
            regex_pattern = regex_pattern.replace(r"\*", ".*")

        # Compile with case-insensitive flag, use fullmatch to match entire string
        compiled = re.compile(regex_pattern, re.IGNORECASE)
        return compiled

    # Convert all patterns to compiled regex objects
    include_patterns = [pattern_to_regex(p) for p in include]
    exclude_patterns = [pattern_to_regex(p) for p in exclude]

    # Check exclude patterns first - if any match, return False
    for pattern in exclude_patterns:
        if pattern.fullmatch(name):
            return False

    # If no include patterns, everything is included by default
    if not include_patterns:
        return True

    # If include patterns exist, name must match at least one
    for pattern in include_patterns:
        if pattern.fullmatch(name):
            return True

    return False
