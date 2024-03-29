#!/bin/sh

python3 -m venv env
. env/bin/activate

sqlite3 olist.db < database_building/create_table.sql
sqlite3 olist.db < database_building/import_table.sql 2>/dev/null