#!/usr/bin/ bash
CURRENT_DIR=`pwd`
docker run --rm --name dd-cmd-02 -v $CURRENT_DIR/db:/opt/app/db dd/cmd:latest