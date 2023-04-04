#!/usr/bin/sh

cd user-control
make down
cd ..

cd iam-gateway
make down
cd ..

cd artifacts
make down
cd ..

cd training
make down
cd ..

cd api-gateway
make down
cd ..
