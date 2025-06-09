#!/bin/bash
# -*- coding: utf-8 -*-

docker run --rm --name mcp-ohmy-sql-dev-psql -p 40311:5432 -e POSTGRES_PASSWORD=password -d postgres:15.7-alpine
sleep 1