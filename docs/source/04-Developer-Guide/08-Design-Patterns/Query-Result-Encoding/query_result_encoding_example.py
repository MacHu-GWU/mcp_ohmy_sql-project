# -*- coding: utf-8 -*-

import json
from pathlib import Path

import tabulate
from faker import Faker

dir_here = Path(__file__).absolute().parent

fake = Faker()
n_rows = 200

rows = list()
for i in range(1, 1+n_rows):
    id = i
    name = fake.name()
    email = fake.email()
    address = fake.address()
    create_time = fake.date_time().strftime("%Y-%m-%d %H:%M:%S")
    row = dict(
        id=id,
        name=name,
        email=email,
        address=address.replace("\n", ", "),
        create_time=create_time,
    )
    rows.append(row)


columns = ["id", "name", "email", "address", "create_time"]

tb = tabulate.tabulate(
    [tuple(row.values()) for row in rows],
    headers=columns,
    tablefmt="pipe",
)
path_markdown = dir_here / "01_markdown_table.md" # 9,621 tokens
path_markdown.write_text(str(tb))

lines = list()
for row in rows:
    line = json.dumps(row, ensure_ascii=False) # 12,305 tokens
    lines.append(line)

path_ndjson = dir_here / "02_ndjson_table.ndjson"
path_ndjson.write_text("\n".join(lines))
