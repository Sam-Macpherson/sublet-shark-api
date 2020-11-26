#!/bin/bash

set -e

if [ $# -lt 3 ]; then
    echo "Usage: init_dbs.sh db_name user password"
    exit 1
fi
echo ""
echo "You are about to create the database '$1' and the user '$2'."
echo ""
read -p "Press [Enter] key to continue or press [CTRL+C] to exit now..." || true

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd "${DIR}" > /dev/null || { echo "Failure"; exit 1; }

echo "Creating user '$2' and database '$1'..."
sudo -u postgres psql -a \
    -v p_dbname="$1" \
    -v p_user="$2" \
    -v p_pass=\'"$3"\' \
    -f init_dbs.sql

echo "Granting privileges on '$1' to user '$2'..."
sudo -u postgres psql -d "$1" -a \
    -v p_dbname="$1" \
    -v p_user="$2" \
    -f grant.sql

popd > /dev/null || { echo "Failure"; exit 1; }

echo "DONE."
