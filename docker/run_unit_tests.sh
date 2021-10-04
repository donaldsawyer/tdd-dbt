#!/bin/bash
set -e

docker/initialize_mssql.sh

for f in docker/dbt_tests/*.sh; do
  echo "#######################################################################"
  echo "Executing tests in $f"
  echo "#######################################################################"

  if ! bash "$f"; then break; fi
done
