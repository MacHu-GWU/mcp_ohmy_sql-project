# -*- coding: utf-8 -*-

aws_region = "us-east-1"
aws_profile = "esc_app_dev_us_east_1"

_name = "mcp-ohmy-sql-dev"
stack_name = _name
redshift_security_group_name = f"{_name}-rs-sg"
redshift_iam_role_name = f"{_name}-rs-iam-role"
workgroup_name = _name
namespace_name = _name
database_name = "dev"
