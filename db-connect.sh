#!/bin/sh
set -e

usage() {
	echo "Usage: $(basename "$0") [-i <interface>] [--interface <interface>]"
	echo "Options:"
	echo "  -i, --interface: Interface to use (psql or pgcli) (default: psql)"
	exit 1
}

interface="psql"

while [ "$#" -gt 0 ]
do
	case "$1" in
		-i | --interface)
			interface="$2";
			shift
			;;
		*)
			usage
			;;
	esac
	shift
done

. ./.env

uri="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$DB_HOST:$DB_PORT/$POSTGRES_DB"

case "$interface" in
	psql)
		psql "$uri"
		;;
	pgcli)
		pgcli "$uri"
		;;
	*)
		echo "Error: Invalid interface specified."
		echo "Please choose either 'psql' or 'pgcli'."
		exit 1
		;;
esac
