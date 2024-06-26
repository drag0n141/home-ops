#!/usr/bin/env bash

set -o nounset
set -o errexit

config_filename="$(date "+%Y%m%d-%H%M%S").xml"

http_host=${S3_URL#*//}
http_host=${http_host%:*}
http_request_date=$(date -R)
http_filepath="${S3_BUCKET}/${config_filename}"
http_signature=$(
    printf "PUT\n\ntext/xml\n%s\n/%s" "${http_request_date}" "${http_filepath}" \
        | openssl dgst -sha1 -hmac "${AWS_SECRET_ACCESS_KEY}" -binary \
        | base64
)

echo "Download Opnsense config file ..."
curl -kfsSL \
    --user "${OPNSENSE_KEY}:${OPNSENSE_SECRET}" \
    --output "/tmp/${config_filename}" \
    "${OPNSENSE_URL}/api/core/backup/download/this"

/bin/ls -l "/tmp/${config_filename}"

echo "Upload backup to s3 bucket ..."
curl -fsSL \
    -X PUT -T "/tmp/${config_filename}" \
    -H "Host: ${http_host}" \
    -H "Date: ${http_request_date}" \
    -H "Content-Type: text/xml" \
    -H "Authorization: AWS ${AWS_ACCESS_KEY_ID}:${http_signature}" \
    "${S3_URL}/${http_filepath}"
