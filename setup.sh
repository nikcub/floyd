#!/bin/bash

FLOYD_PATH="$( cd "$( dirname "$0" )" && pwd )"
FLOYD_BIN_PATH="$FLOYD_PATH/bin"

echo "export PATH=\"$FLOYD_BIN_PATH:\$PATH\"" >> ~/.bash_profile
source ~/.bash_profile
 