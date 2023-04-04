#!/usr/bin/sh

cd user-control
make &
cd ..

cd iam-gateway
make &
cd ..

cd artifacts
make &
cd ..

cd training
make &
cd ..

cd api-gateway
make &
cd ..
