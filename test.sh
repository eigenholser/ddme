#!/bin/sh

curl localhost:3000/book | json_reformat
curl localhost:3000/sell --data '{"qty":10,"prc":15}' -H "Content-Type: application/json"
curl localhost:3000/sell --data '{"qty":10,"prc":13}' -H "Content-Type: application/json"
curl localhost:3000/buy  --data '{"qty":10,"prc":7}' -H "Content-Type: application/json"
curl localhost:3000/buy  --data '{"qty":10,"prc":9.5}' -H "Content-Type: application/json"
curl localhost:3000/book | json_reformat
curl localhost:3000/sell --data '{"qty":5, "prc":9.5}' -H "Content-Type: application/json"
curl localhost:3000/book | json_reformat
curl localhost:3000/buy  --data '{"qty":6, "prc":13}' -H "Content-Type: application/json"
curl localhost:3000/book | json_reformat
curl localhost:3000/sell --data '{"qty":7, "prc":7}' -H "Content-Type: application/json"
curl localhost:3000/book | json_reformat
curl localhost:3000/sell --data '{"qty":12, "prc":6}' -H "Content-Type: application/json"
curl localhost:3000/book | json_reformat
