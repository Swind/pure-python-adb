#!/usr/bin/env sh
git tag v1.0.$3
devpi use http://192.168.1.82:3141/cloudmosa/dev
devpi login $1 --password=$2

rm -rf sdisk
python3 setup.py sdist
devpi upload dist/*.tar.gz
