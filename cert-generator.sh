#!/bin/bash

# Get the IP address
IP_ADDRESS=$(hostname -I | cut -d' ' -f1)

# Generate SSL certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout key.pem -out cert.pem \
    -subj "/CN=$IP_ADDRESS" \
    -addext "subjectAltName=IP:$IP_ADDRESS"

# Copy the certificate
cat cert.pem key.pem > localhost.pem

echo "Certificate generated for IP: $IP_ADDRESS"