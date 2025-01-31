#!/bin/bash
# run_synthea.sh: Script to generate synthetic data using Synthea and export to CSV
#
# Arguments:
# $1: The population size to generate
# $2: The output directory to save the synthetic data
# $3: The state to generate the synthetic data for
# $4: The city to generate the synthetic data for
# $5: The gender distribution (optional) - note: removed from command line
# $6: The race distribution (optional)
# $7: The age distribution (optional)
# $8: The socioeconomic status distribution (optional)
# $9: The living conditions distribution (optional)
# $10: The split records flag to enable splitting records

set -e

# ./run_synthea.sh
# Check if synthea jar exists
JAR_PATH="../assets/synthea-with-dependencies.jar"

SIZE=${1:-"10"} # 1,596,273 population
OUTPUT_DIR=${2:-"./data/"}
STATE=${3:-"New York"}
CITY=${4:-"New York"}
GENDER_DIST=${5:-"47.8:52.2"} # Default is 50% male, 50% female
RACE_DIST=${6:-"44.5:11.9:26.2:12.4"} # Default is 60% White, 20% Black, 10% Hispanic, 10% Asian
AGE_DIST=${7:-"16.3:59.9:18.9:4.8"} # Default is 20% children, 30% adults, 25% seniors, 25% elderly
SES_DIST=${8:-"32.1:19.1:22:26.7"} # Default is 30% low, 30% middle, 20% high, 20% very high socioeconomic status
LIVING_COND_DIST=${9:-"100:0"} # Default is 50% urban, 50% rural
SPLIT=${10:-"0"}

# Create split records argument
case $SPLIT in
    1|t|T|true|TRUE)
        SPLIT_RECORDS_ARG="--exporter.split_records=true"
        ;;
    *)
        SPLIT_RECORDS_ARG="--exporter.split_records=false"
        ;;
esac

mkdir -p "${OUTPUT_DIR}"
rm -rf "${OUTPUT_DIR}"/*

# Path to the synthea.properties file
CONFIG_FILE="../assets/synthea.properties"

# Run Synthea with parameters for seeding, the population size, and various distributions.
# Additionally disable generating hospital and practitioner FHIR resources, as we only
# want patient data and limit the results to only alive patients.
# For a full list of parameters, see the
# [configuration file](https://github.com/synthetichealth/synthea/blob/master/src/main/resources/syqnthea.properties).

java -jar $JAR_PATH --exporter.csv.export=true \
    --exporter.hospital.fhir.export false \
    --exporter.practitioner.fhir.export false \
    --exporter.fhir.export  false \
    $SPLIT_RECORDS_ARG \
    --exporter.split_records.duplicate_data=true \
    --exporter.csv.fileName "patients.csv" \
    --exporter.baseDirectory "${OUTPUT_DIR}" \
    --config "${CONFIG_FILE}" \
    -p "${SIZE}" -s "1" -cs "1" \
    "${STATE}" "${CITY}" | grep -v "Loading" # silence the "Loading..." messages --exporter.csv.export=true \