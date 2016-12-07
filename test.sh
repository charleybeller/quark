#!/bin/bash

set -e

cwd=$(pwd)

set -x

javac -version
java -version
type python
python -c 'import sys; print(sys.version); sys.exit(int(sys.version_info[:3] < (2,7,6) or (3,0,0) < sys.version_info[:3]))'
node --version
ruby --version
mvn --version

if flake8 quarkc; then
    echo flake8 passed
else
    exit 1
fi

#if pylint quarkc; then
#    echo pylint passed
#else
#    exit 1
#fi

if py.test --durations=10 && quark-test run --stats quarkc/test/e2e/*.q quarkc/test/e2e/*.ir; then
    echo Tests passed
else
    ./quarkc/test/compare --batch
    exit 1
fi