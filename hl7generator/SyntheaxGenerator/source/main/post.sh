#!/bin/bash

# Define variables, enter output directory
OUTPUT_DIR=""
TOKEN_URL="http://localhost:8100/realms/NBS/protocol/openid-connect/token"
INGESTION_API="http://localhost:8081/ingestion/api/elrs"
STATUS_API="http://localhost:8081/ingestion/api/elrs/status-details"
CLIENT_ID="di-keycloak-client"
CLIENT_SECRET="OhBq1ar96aep8cnirHwkCNfgsO9yybZI"
POST_HEADERS=(
  "-H" "clientid: $CLIENT_ID"
  "-H" "clientsecret: $CLIENT_SECRET"
  "-H" "version: 2"
  "-H" "Content-Type: text/plain"
  "-H" "msgType: HL7"
  "-H" "validationActive: true"
)
CSV_FILE="$HOME/response_log.csv"

# Create CSV file and add headers
echo "FileName,PostResponse,StatusResponse" > "$CSV_FILE"

# Retrieve the token
TOKEN_RESPONSE=$(curl -s -X POST "$TOKEN_URL" \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET")

# Extract the token (the field is 'access_token' in the response)
TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.access_token')

# Check if token retrieval succeeded
if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
  echo "Error: Failed to retrieve authentication token."
  exit 1
fi

# Process .txt files in the output directory
for FILE in "$OUTPUT_DIR"/*.txt; do
  if [[ -f "$FILE" ]]; then
    echo "Processing file: $FILE"
    POST_RESPONSE=$(curl -s -X POST "$INGESTION_API" \
      "${POST_HEADERS[@]}" \
      -H "Authorization: Bearer $TOKEN" \
      --data-binary "@$FILE")

    # Print the raw response for debugging
    echo "Raw POST Response: $POST_RESPONSE"

    # Treat the response as a string ID (messageUuid)
    MESSAGE_UUID="$POST_RESPONSE"

    # Default status response
    STATUS_RESPONSE="N/A"

    # Fetch status details if messageUuid exists
    if [[ -n "$MESSAGE_UUID" && "$MESSAGE_UUID" != "null" ]]; then
      STATUS_RESPONSE=$(curl -s -X GET "$STATUS_API/$MESSAGE_UUID?clientid=$CLIENT_ID&clientsecret=$CLIENT_SECRET" \
        -H "Authorization: Bearer $TOKEN")
    fi

    # Log responses to CSV file
    echo "\"$(basename "$FILE")\",\"$POST_RESPONSE\",\"$STATUS_RESPONSE\"" >> "$CSV_FILE"

    echo "Responses for $FILE saved to $CSV_FILE"
  else
    echo "No .txt files found in $OUTPUT_DIR."
  fi
done
