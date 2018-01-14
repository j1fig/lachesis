#!/bin/bash

VERSION="0.1.0"
TAG="j1fig/lachesis-notebook:$VERSION"

echo Building lachesis-notebook v$VERSION ...

docker build -t $TAG .
docker push $TAG

echo Done!
