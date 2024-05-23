#!/bin/sh
set -e

all_endpoints() {
	echo 'register/doctor/'
}

usage() {
	set +xe
	echo "Usage: $(basename "$0") [endpoint|all]"
	echo 'All endpoints:'
	echo
	all_endpoints | sed 's/^/-  /'
	exit 1
}

[ $# -eq 0 ] && usage

if [ "$1" = all ]
then
	all_endpoints | xargs "$0"
	exit 0
fi

. ./.env

for arg
do
	user_name="$(faker --lang pt_PT user_name)"
	name="$(faker --lang pt_PT name)"
	email="$(faker --lang pt_PT email)"
	password="$(faker --lang pt_PT password)"
	license_key="$(faker --lang pt_PT job)"

	url="http://$SERVER_HOST:$SERVER_PORT/$arg"

	(
	set -xe
	case "$arg" in
		register/doctor/)
			curlie post "$url" \
				contract_details="doctor graduated at University of Coimbra" \
				email="$email" \
				license="$license_key" \
				name="$name" \
				password="$password" \
				username="$user_name"
			;;
		*) usage ;;
	esac
	)
done
