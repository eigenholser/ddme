#!/bin/sh

port=$1
if [ -z $port ]; then
    port=3000
fi

if [ ! -z $2 ]; then
    verbose="-v"
fi

echo "***"
curl --silent localhost:$port/book $verbose | json_reformat
echo
echo "***"
curl --silent localhost:$port/sell --data '{"qty":10,"prc":15}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/sell --data '{"qty":10,"prc":13}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/buy  --data '{"qty":10,"prc":7}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/buy  --data '{"qty":10,"prc":9.5}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/book $verbose | json_reformat
echo
echo "***"
curl --silent localhost:$port/sell --data '{"qty":5, "prc":9.5}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/book $verbose | json_reformat
echo
echo "***"
curl --silent localhost:$port/buy  --data '{"qty":6, "prc":13}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/book $verbose | json_reformat
echo
echo "***"
curl --silent localhost:$port/sell --data '{"qty":7, "prc":7}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/book $verbose | json_reformat
echo
echo "***"
curl --silent localhost:$port/sell --data '{"qty":12, "prc":6}' -H "Content-Type: application/json" $verbose
echo
echo
echo "***"
curl --silent localhost:$port/book $verbose | json_reformat
echo
