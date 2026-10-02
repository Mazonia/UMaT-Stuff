#!/bin/bash
# Active Directory BloodHound Ingestion Script for INLANEFREIGHT.LOCAL
DC_IP="172.16.8.3"
DOMAIN="inlanefreight.local"

echo "[+] Executing BloodHound Python Ingester..."
bloodhound-python -u hporter -p 'Gr8hambino!' -d $DOMAIN -ns $DC_IP -c All --zip

echo "[+] Ingestion complete. Upload zip package into BloodHound GUI."
