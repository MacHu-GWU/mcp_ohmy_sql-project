# -*- coding: utf-8 -*-

import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_redshiftserverless as redshiftserverless
from constructs import Construct

import requests


def get_my_ip() -> str:
    res = requests.get("https://checkip.amazonaws.com/")
    return res.text.strip()


class Stack(
    cdk.Stack,
):
    def __init__(
        self,
        scope: Construct,
        id: str,
        stack_name: str,
        env: cdk.Environment,
        vpc_id: str,
        security_group_name: str,
        namespace_name: str,
        db_name: str,
        workgroup_name: str,
    ):
        super().__init__(
            scope=scope,
            id=id,
            stack_name=stack_name,
            env=env,
        )
        self.vpc_id = vpc_id
        self.security_group_name = security_group_name
        self.namespace_name = namespace_name
        self.db_name = db_name
        self.workgroup_name = workgroup_name

        self.create_security_group()
        self.create_namespace()
        self.create_workgroup()

    def create_security_group(self):
        self.vpc = ec2.Vpc.from_lookup(
            scope=self,
            id="MyOhMySqlDevVpc",
            vpc_id=self.vpc_id,
        )
        self.sg = ec2.SecurityGroup(
            scope=self,
            id="MyOhMySqlDevSecurityGroup",
            vpc=self.vpc,
            allow_all_outbound=True,
        )
        my_ip = get_my_ip()
        self.sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(f"{my_ip}/32"),
            connection=ec2.Port.tcp(5439),
        )

    def create_namespace(self):
        """
        Ref: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_redshiftserverless/CfnNamespace.html
        """
        self.namespace = redshiftserverless.CfnNamespace(
            scope=self,
            id="MyOhMySqlDevNamespace",
            namespace_name=self.namespace_name,
            db_name=self.db_name,
        )
        self.namespace.apply_removal_policy(
            cdk.RemovalPolicy.DESTROY,
        )

    def create_workgroup(self):
        """
        Ref: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_redshiftserverless/CfnWorkgroup.html
        """
        selected = self.vpc.select_subnets(subnet_type=ec2.SubnetType.PUBLIC)
        subnet_ids = selected.subnet_ids
        self.workgroup = redshiftserverless.CfnWorkgroup(
            scope=self,
            id="MyOhMySqlDevWorkgroup",
            workgroup_name=self.workgroup_name,
            namespace_name=self.namespace_name,
            base_capacity=8,  # minimal capacity 8 RPUs
            max_capacity=8,
            publicly_accessible=True,
            subnet_ids=subnet_ids,
            security_group_ids=[
                self.sg.security_group_id,
            ],
        )
        self.workgroup.node.add_dependency(self.namespace)
        self.workgroup.node.add_dependency(self.sg)
        self.workgroup.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
