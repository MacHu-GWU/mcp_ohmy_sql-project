.. _aws-redshift-connection-configuration:

AWS Redshift Connection Configuration
==============================================================================
`Amazon Redshift <https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html>`_ is a cloud-based data warehouse service that requires specialized connection configuration. ``mcp_ohmy_sql`` supports both traditional username/password authentication and modern AWS IAM-based authentication for Redshift clusters.

.. seealso::

    :class:`~mcp_ohmy_sql.config.aws_redshift.AWSRedshiftConnection` - The configuration class source code for AWS Redshift connection


AWS Redshift Connection Type
------------------------------------------------------------------------------
AWS Redshift databases use the ``"aws_redshift"`` connection type:

.. code-block:: json

    {
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            // ... authentication configuration
        }
    }


Authentication Methods
------------------------------------------------------------------------------
AWS Redshift supports two main authentication approaches:

1. **Direct Credentials**: Traditional host/port/username/password
2. **AWS IAM Authentication**: Uses AWS credentials and temporary tokens

Both methods ultimately create a SQLAlchemy connection, but handle authentication differently.


Method 1: Direct Credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use this method when you have direct database credentials:

.. code-block:: json

    {
        "identifier": "redshift_direct",
        "description": "Redshift with direct credentials",
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            "host": "my-cluster.abc123.us-east-1.redshift.amazonaws.com",
            "port": 5439,
            "database": "warehouse",
            "username": "analyst", 
            "password": "secure_password"
        }
    }

**Required Fields for Direct Credentials:**

- ``host``: Redshift cluster endpoint
- ``port``: Database port (typically 5439)
- ``database``: Database name within the cluster
- ``username``: Database username
- ``password``: Database password


Method 2: AWS IAM Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use this method for secure, credential-free authentication using AWS IAM:

**For Redshift Clusters:**

.. code-block:: json

    {
        "identifier": "redshift_iam_cluster",
        "description": "Redshift cluster with IAM auth",
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            "cluster_identifier": "my-analytics-cluster",
            "database": "warehouse",
            "boto_session_kwargs": {
                "region_name": "us-east-1",
                "profile_name": "analytics"
            }
        }
    }

**For Redshift Serverless:**

.. code-block:: json

    {
        "identifier": "redshift_serverless",
        "description": "Redshift Serverless with IAM auth",  
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            "namespace_name": "analytics-namespace",
            "workgroup_name": "analytics-workgroup",
            "boto_session_kwargs": {
                "region_name": "us-west-2",
                "profile_name": "default"
            }
        }
    }


AWS Credentials Configuration
------------------------------------------------------------------------------
The ``boto_session_kwargs`` object configures how to authenticate with AWS:

.. code-block:: json

    {
        "boto_session_kwargs": {
            "region_name": "us-east-1",
            "profile_name": "analytics",
            "aws_access_key_id": "AKIA...",
            "aws_secret_access_key": "...",
            "aws_session_token": "...",
            "role_arn": "arn:aws:iam::123456789012:role/RedshiftAnalyst",
            "duration_seconds": 3600,
            "auto_refresh": false
        }
    }

**AWS Credential Options:**

.. list-table:: AWS Credential Parameters
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``region_name``
     - No
     - AWS region where Redshift cluster is located
   * - ``profile_name``
     - No
     - AWS CLI profile name from ``~/.aws/credentials``
   * - ``aws_access_key_id``
     - No
     - AWS access key (use environment variables instead)
   * - ``aws_secret_access_key``
     - No
     - AWS secret key (use environment variables instead)
   * - ``aws_session_token``
     - No
     - Temporary session token for STS credentials
   * - ``role_arn``
     - No
     - IAM role to assume for Redshift access
   * - ``duration_seconds``
     - No
     - Session duration when assuming roles (default: 3600)
   * - ``auto_refresh``
     - No
     - Automatically refresh temporary credentials (default: false)


Complete Configuration Examples
------------------------------------------------------------------------------
**Development with Direct Credentials:**

.. code-block:: json

    {
        "identifier": "redshift_dev",
        "description": "Development Redshift cluster",
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            "host": "dev-cluster.abc123.us-east-1.redshift.amazonaws.com",
            "port": 5439,
            "database": "dev_warehouse",
            "username": "dev_user",
            "password": "dev_password"
        },
        "schemas": [
            {
                "name": "public",
                "table_filter": {
                    "exclude": ["temp_*", "staging_*"]
                }
            }
        ]
    }

**Production with IAM Authentication:**

.. code-block:: json

    {
        "identifier": "redshift_prod",
        "description": "Production analytics warehouse",
        "db_type": "aws_redshift", 
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy",
            "cluster_identifier": "prod-analytics-cluster",
            "database": "warehouse",
            "boto_session_kwargs": {
                "region_name": "us-east-1",
                "profile_name": "production"
            }
        },
        "schemas": [
            {
                "name": "public",
                "table_filter": {
                    "exclude": ["staging_*", "temp_*", "admin_*"]
                }
            },
            {
                "name": "marts",
                "table_filter": {
                    "include": ["fact_*", "dim_*", "*_summary"]
                }
            }
        ]
    }

**Cross-Account Role Assumption:**

.. code-block:: json

    {
        "identifier": "redshift_cross_account",
        "description": "Cross-account Redshift access",
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift", 
            "method": "sqlalchemy",
            "cluster_identifier": "shared-analytics",
            "database": "warehouse",
            "boto_session_kwargs": {
                "region_name": "us-east-1",
                "role_arn": "arn:aws:iam::987654321098:role/CrossAccountRedshiftAccess",
                "duration_seconds": 7200,
                "auto_refresh": true
            }
        }
    }

**Redshift Serverless Configuration:**

.. code-block:: json

    {
        "identifier": "redshift_serverless_analytics",
        "description": "Serverless analytics workgroup",
        "db_type": "aws_redshift",
        "connection": {
            "type": "aws_redshift",
            "method": "sqlalchemy", 
            "namespace_name": "analytics-ns",
            "workgroup_name": "analytics-wg",
            "boto_session_kwargs": {
                "region_name": "us-west-2",
                "profile_name": "serverless"
            }
        },
        "schemas": [
            {
                "name": "analytics",
                "table_filter": {
                    "include": ["daily_*", "monthly_*", "summary_*"]
                }
            }
        ]
    }


AWS IAM Permissions
------------------------------------------------------------------------------
For IAM authentication to work, your AWS credentials need appropriate permissions:

**Required IAM Permissions for Redshift Clusters:**

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "redshift:DescribeClusters",
                    "redshift:GetClusterCredentialsWithIAM"
                ],
                "Resource": [
                    "arn:aws:redshift:region:account:cluster/cluster-name",
                    "arn:aws:redshift:region:account:dbuser:cluster-name/username"
                ]
            }
        ]
    }

**Required IAM Permissions for Redshift Serverless:**

.. code-block:: json

    {
        "Version": "2012-10-17", 
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "redshift-serverless:GetNamespace",
                    "redshift-serverless:GetWorkgroup",
                    "redshift-serverless:GetCredentials"
                ],
                "Resource": [
                    "arn:aws:redshift-serverless:region:account:namespace/namespace-id"
                ]
            }
        ]
    }


Security Best Practices
------------------------------------------------------------------------------
**Use IAM Authentication:**

Prefer IAM authentication over hardcoded credentials:

.. code-block:: json

    // ✅ Recommended: IAM authentication
    {
        "boto_session_kwargs": {
            "region_name": "us-east-1",
            "profile_name": "analytics"
        }
    }

    // ❌ Avoid: Hardcoded credentials
    {
        "username": "user",
        "password": "hardcoded_password"
    }

**Environment Variables:**

Use environment variables for sensitive data:

.. code-block:: bash

    export AWS_PROFILE=analytics
    export AWS_REGION=us-east-1

**Credential Hierarchy:**

AWS credentials are resolved in this order:

1. Explicit credentials in ``boto_session_kwargs``
2. Environment variables (``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``)
3. AWS CLI profiles (``~/.aws/credentials``)
4. IAM instance profiles (for EC2)
5. IAM container credentials (for ECS)


Troubleshooting
------------------------------------------------------------------------------
**Common Issues:**

1. **Authentication failures**: Check AWS credentials and IAM permissions
2. **Network connectivity**: Verify security groups and VPC settings
3. **Cluster not found**: Check cluster identifier and region
4. **SSL errors**: Redshift requires SSL connections
5. **Token expiration**: Use ``auto_refresh`` for long-running sessions

**Testing AWS Credentials:**

Test your AWS credentials independently:

.. code-block:: bash

    aws redshift describe-clusters --region us-east-1
    aws sts get-caller-identity


AWS Redshift Documentation
------------------------------------------------------------------------------
For comprehensive information about AWS Redshift configuration and best practices:

- `AWS Redshift Getting Started <https://docs.aws.amazon.com/redshift/latest/gsg/>`_
- `Redshift Database User Authentication <https://docs.aws.amazon.com/redshift/latest/mgmt/generating-user-credentials.html>`_
- `Redshift IAM Authentication <https://docs.aws.amazon.com/redshift/latest/mgmt/redshift-iam-authentication-access-control.html>`_
- `Redshift Serverless <https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-serverless.html>`_
- `AWS CLI Configuration <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>`_

The ``mcp_ohmy_sql`` server leverages AWS SDKs and follows AWS best practices for authentication and security.


Next Steps
------------------------------------------------------------------------------
- :ref:`schema-configuration` - Configure schemas and table filtering for your Redshift warehouse
- :ref:`relational-database-connection-configuration` - Learn about SQLAlchemy-based connections
- :ref:`connection-configuration` - Return to connection configuration overview
