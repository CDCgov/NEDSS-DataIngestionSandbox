#!/bin/ksh

SRC_DIR=$HOME/projects/nbsadapter/hl7-data-files/ELR-ExampleMessages/Elr-ExampleMessages-1.9.2-012216
DKR_DIR=/tmp/hl7files
SLEEP_INTERVAL=10

echo "This script copies hl7 test files every $SLEEP_INTERVAL seconds to target directory"

for ii in `ls $SRC_DIR`
do
  echo "Copying $ii to $DKR_DIR"
  cp $SRC_DIR/$ii $DKR_DIR/$ii.hl7

  echo "Will wait $SLEEP_INTERVAL seconds before resuming"
  sleep $SLEEP_INTERVAL
done


