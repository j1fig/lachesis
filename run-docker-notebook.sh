#!/bin/bash

VERSION="0.1.0"
TAG="j1fig/lachesis-notebook:$VERSION"

docker pull $TAG

docker run  --volume `pwd`:/root/workdir --workdir /root/workdir -it --rm -p 127.0.0.1:8888:8888 $TAG
