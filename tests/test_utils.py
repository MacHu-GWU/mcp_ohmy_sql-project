# -*- coding: utf-8 -*-

from mcp_ohmy_sql.utils import match


def test_match():
    # Test case-insensitive matching
    assert match("EMPLOYEES", ["employees"], []) == True
    assert match("employees", ["EMPLOYEES"], []) == True
    assert match("EmPlOyEeS", ["employees"], []) == True
    
    # Test no match with include patterns
    assert match("EMPLOYEES", ["managers"], []) == False
    assert match("EMPLOYEES", ["departments", "managers"], []) == False
    
    # Test empty include list (everything included by default)
    assert match("EMPLOYEES", [], []) == True
    assert match("anything", [], []) == True
    assert match("random_table", [], []) == True
    
    # Test exclude patterns override include
    assert match("EMPLOYEES", ["employees"], ["employees"]) == False
    assert match("EMPLOYEES", [], ["employees"]) == False
    assert match("EMPLOYEES", ["*"], ["employees"]) == False
    
    # Test wildcard patterns
    assert match("EMPLOYEES", ["EMPLOYEE*"], []) == True
    assert match("EMPLOYEE_HISTORY", ["EMPLOYEE*"], []) == True
    assert match("MANAGERS", ["EMPLOYEE*"], []) == False
    assert match("EMPLOYEES", ["*EES"], []) == True
    assert match("TREES", ["*EES"], []) == True
    assert match("EMPLOYEES", ["*"], []) == True
    
    # Test regex patterns (fullmatch means pattern must match entire string)
    assert match("EMPLOYEES", ["^EMPLOYEES$"], []) == True
    assert match("EMPLOYEES", ["^EMP.*"], []) == True
    assert match("MANAGERS", ["^EMP.*"], []) == False
    assert match("EMPLOYEES", [".*EES$"], []) == True
    assert match("EMPLOYEE", [".*EES$"], []) == False
    
    # Test multiple include patterns (OR logic)
    assert match("EMPLOYEES", ["managers", "employees"], []) == True
    assert match("MANAGERS", ["managers", "employees"], []) == True
    assert match("DEPARTMENTS", ["managers", "employees"], []) == False
    
    # Test multiple exclude patterns
    assert match("EMPLOYEES", [], ["managers", "employees"]) == False
    assert match("MANAGERS", [], ["managers", "employees"]) == False
    assert match("DEPARTMENTS", [], ["managers", "employees"]) == True
    
    # Test complex scenarios
    assert match("EMPLOYEE_HISTORY", ["EMPLOYEE*"], ["*_HISTORY"]) == False
    assert match("EMPLOYEE_CURRENT", ["EMPLOYEE*"], ["*_HISTORY"]) == True
    assert match("MANAGER_HISTORY", ["*"], ["*_HISTORY", "*_TEMP"]) == False
    assert match("MANAGER_CURRENT", ["*"], ["*_HISTORY", "*_TEMP"]) == True
    
    # Test edge cases
    assert match("", [""], []) == True
    assert match("", ["*"], []) == True
    assert match("test", [""], []) == False
    assert match("", [], ["*"]) == False
    
    # Test literal dot matching (wildcard mode)
    assert match("test.table", ["test.table"], []) == True
    assert match("testtable", ["test.table"], []) == False
    
    # Test regex mode with special characters
    assert match("test+table", ["test\\+table"], []) == True
    assert match("testtable", ["test+table"], []) == True  # + means one or more in regex
    assert match("test[1]", ["test\\[1\\]"], []) == True
    assert match("test1", ["test[1]"], []) == True  # [1] is a character class in regex
    
    # Test pattern priority (exclude overrides include)
    assert match("EMPLOYEES", ["EMPLOYEE*", "EMP*"], ["*EES"]) == False
    assert match("EMPLOYEE", ["EMPLOYEE*", "EMP*"], ["*EES"]) == True
    
    # Additional edge cases
    assert match("test", ["*"], ["*"]) == False  # Exclude everything
    assert match("table_name", ["table_*"], ["*_temp", "*_tmp"]) == True
    assert match("table_temp", ["table_*"], ["*_temp", "*_tmp"]) == False
    assert match("TABLE_TEMP", ["table_*"], ["*_TEMP", "*_tmp"]) == False  # Case insensitive
    
    # Test combining regex and wildcard patterns
    assert match("EMPLOYEES", ["^EMP.*", "MANAGER*"], []) == True
    assert match("MANAGERS", ["^EMP.*", "MANAGER*"], []) == True
    assert match("DEPARTMENTS", ["^EMP.*", "MANAGER*"], []) == False
    
    # Test escaped wildcards in table names (rare but possible)
    assert match("table*name", ["table\\*name"], []) == True
    assert match("tablename", ["table\\*name"], []) == False


if __name__ == "__main__":
    from mcp_ohmy_sql.tests import run_cov_test

    run_cov_test(
        __file__,
        "mcp_ohmy_sql.utils",
        preview=False,
    )
