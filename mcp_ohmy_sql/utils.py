# -*- coding: utf-8 -*-

def match(
    name: str,
    include: list[str],
    exclude: list[str],
) -> bool:
    """
    Match a name against include and exclude lists.

    The include/exclude pattern system works like a two-stage filter where name
    must pass both inclusion and exclusion criteria to be selected for processing.

    - Default inclusion: any name are initially included unless specific
        include patterns are provided, then name must match at least one
        include pattern to qualify
    - Include matching: When include patterns exist, a name needs to match
        ANY of the include patterns (logical OR) to be considered for selection
    - Exclude override: If exclude patterns exist and a name matches ANY
        exclude pattern, it gets removed from the results regardless of whether
        it matched include patterns

    Include pattern can be regular expressions like `^EMPLOYEES`, `EMPLOYEE*`

    And the match is case insensitive.
    """