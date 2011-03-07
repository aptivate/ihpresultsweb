#!/bin/sh

if [ -z "$2" ]; then
	echo "Usage: $0 <sqlite-dump-file> <mysql-output-sql-file>" >&2
	exit 2
fi

perl -pe '
s/BEGIN TRANSACTION;/set sql_mode="ANSI";/;
s/(CREATE TABLE|INSERT INTO|REFERENCES|CREATE INDEX|ON) "([^"]*)"/\1 \2/g;
# s/^    "([^"]+)"/    `\1`/;
# m/(UNIQUE|REFERENCES \S+|ON \S+) \((.*)\)/ and s/"//g;
s/ bool / boolean /g;
s/`id` integer NOT NULL PRIMARY KEY/`id` int4 not null auto_increment primary key/;
s/submissions_countryscorecardoverridecomments_country_id__language_id/unique_country_id_language_id/;
' < $1 > $2
