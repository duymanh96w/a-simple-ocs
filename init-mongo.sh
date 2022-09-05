#!/bin/bash
mongo --host mongodb --port 27017 -- ${DB_NAME} <<EOF
db.createCollection("billing_info");
db.billing_info.createIndex({"username": 1})
EOF