#!/bin/bash

set -e

if [ $# -lt 1 ]; then
    echo "Usage: drop_dbs.sh db_name user"
    exit 1
fi

echo ""
echo "You are about to drop the database '$1' and user '$2'."
echo ""
read -p "Press [Enter] key to continue or press [CTRL+C] to exit now..." || true

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd "${DIR}" > /dev/null || { echo "Failure"; exit 1; }

echo "Dropping database '$1' and user '$2'..."
sudo -u postgres psql -a -v p_dbname="$1" -v p_user="$2" -f drop_dbs.sql

popd > /dev/null || { echo "Failure"; exit 1; }

echo "DONE."
