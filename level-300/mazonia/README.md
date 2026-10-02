# Simulated Privilege Escalation & Domain Compromise (INLANEFREIGHT.LOCAL)

![Course Banner](https://img.shields.io/badge/Course-CY376%3A%20Network%20Monitoring%2C%20Security%20%26%20Auditing-1F4E79?style=for-the-badge)
![Track](https://img.shields.io/badge/Track-Red%20Team%20Penetration%20Testing-C00000?style=for-the-badge)
![Target](https://img.shields.io/badge/Target-INLANEFREIGHT.LOCAL-2F5597?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete%20Domain%20Compromise%20(DCSync)-385723?style=for-the-badge)

## Project Overview

This repository contains the full source code, scripts, configuration files, evidence logs, screenshots, and technical documentation for the end-of-semester Red Team project: **Simulated Privilege Escalation & Domain Compromise**.

Operating under an **assumed-breach threat model**, the assessment demonstrated how an initial low-privileged domain user (`hporter : Gr8hambino!`) could systematically discover, chain, and exploit 10 distinct Active Directory misconfigurations across 12 operational stages to achieve 100% domain takeover via DCSync (`NTDS.DIT` credential replication) without relying on zero-day exploits.

---

## Student Information

| Attribute | Details |
|---|---|
| **Student Name** | Enoch Nana Tabi Oduro |
| **Course Code** | CY376: Network Monitoring, Security and Auditing |
| **Project Track** | Red Team Assumed-Breach Penetration Test |
| **Submission Date** | Monday, 3rd August 2026 |
| **GitHub Repository** | [privilege-escalation-n-dom-compromise](https://github.com/Mazonia/privilege-escalation-n-dom-compromise) |

---

## Key Assessment Results & Statistics

- **Initial Access**: Low-privileged domain user (`hporter`)
- **Final Privilege Achieved**: Domain Administrator / DCSync (`INLANEFREIGHT\Administrator`)
- **Total Attack Chain Stages**: 12 Sequential Stages
- **Misconfigurations Chained**: 10 Structural & Delegated Flaws
- **Target Domain Controller**: `DC01` (`172.16.8.3`)
- **Target Member Server**: `MS01` (`172.16.8.50`)
- **Full Report & Slides**: Available in [`docs/INLANEFREIGHT_AD_Compromise_Report.docx`](docs/INLANEFREIGHT_AD_Compromise_Report.docx), [`docs/INLANEFREIGHT_AD_Compromise_Report.pdf`](docs/INLANEFREIGHT_AD_Compromise_Report.pdf), and [`docs/INLANEFREIGHT_AD_Compromise_Presentation.pptx`](docs/INLANEFREIGHT_AD_Compromise_Presentation.pptx)

---

## Repository Structure

```
privilege-escalation-n-dom-compromise/
├── README.md                      # Primary project overview, setup, and attack chain walkthrough
├── .gitignore                     # Git exclusion rules for secrets, large captures, and venvs
├── docs/                          # Report and 10-minute presentation slides submissions
│   ├── INLANEFREIGHT_AD_Compromise_Report.docx
│   ├── INLANEFREIGHT_AD_Compromise_Report.pdf
│   └── INLANEFREIGHT_AD_Compromise_Presentation.pptx
├── scripts/                       # Red Team execution scripts and automation playbooks
│   ├── attack_chain_playbook.sh   # Full CLI command invocation playbook
│   ├── bloodhound_enum.sh         # AD LDAP graph enumeration script
│   └── dcsync_dump.py             # PoC DCSync replication runner
├── configs/                       # Target environment configuration files
│   ├── lab_topology.json          # Lab network subnet and host mapping
│   └── audit_policy.xml           # Active Directory audit policy baseline
└── evidence/                      # Sanitized logs and visual evidence
    ├── logs/                      # Raw tool execution logs
    │   ├── bloodhound_summary.log
    │   ├── getuserspns_tgs.log
    │   └── secretsdump_ntds.log
    └── screenshots/               # Annotated evidence screenshots (Figures 1 - 21)
        ├── fig01_initial_foothold.png
        ├── fig02_bloodhound_acl.png
        └── ...
```

---

## Tools Used & Rationale

| Tool | Category | Operational Functionality |
|---|---|---|
| **NetExec (`nxc`)** | SMB / WinRM Scanner | SMB credential verification, share enumeration, share spidering (`spider_plus`). |
| **BloodHound & `bloodyAD`** | AD Graph & ACL Tooling | LDAP directory ingestion, hidden ACL path analysis, and object permission editing. |
| **`evil-winrm`** | WinRM Shell Client | Remote interactive PowerShell sessions over Windows Remote Management (Port 5985). |
| **Impacket Suite** | Protocol Exploitation | `GetUserSPNs.py` (Kerberoasting) and `secretsdump.py` (DCSync replication). |
| **Mimikatz** | LSASS & Memory Analysis | Extracting cleartext autologon registry secrets (`lsadump::secrets`) on MS01. |
| **Hashcat** | Offline Password Cracker | GPU-accelerated offline cracking of Kerberos TGS hashes (Mode 13100 / RC4-HMAC). |
| **`xfreerdp`** | RDP Client | Graphical desktop access to member server MS01 for service configuration. |

---

## 12-Stage Attack Chain Summary

1. **Initial Foothold Verification**: Authenticated `hporter : Gr8hambino!` via SMB against DC01 (`172.16.8.3`).
2. **BloodHound Enumeration**: Ingested AD data; identified `hporter` possessed `ForceChangePassword` over `ssmalls`.
3. **Abuse ForceChangePassword ACL**: Reset `ssmalls` password to `mazoniakid` using `bloodyAD`.
4. **File Share Credential Harvesting**: Spidered IT department share as `ssmalls`; extracted `backupadm : !qazXSW@` from `SQL Express Backup.ps1`.
5. **WinRM Host Discovery & Lateral Movement**: Authenticated to member server MS01 (`172.16.8.50`) via WinRM as `backupadm`.
6. **Leftover Deployment Artifact Exposure**: Discovered cleartext `ilfserveradm : Sys26Admin` setup credentials in `C:\panther\unattend.xml`.
7. **Local Privilege Escalation (MS01)**: Exploited vulnerable Sysax Automation service to execute `net localgroup administrators ilfserveradm /add` as `SYSTEM`.
8. **LSA Secrets Dump**: Extracted autologon registry secrets via Mimikatz to capture `mssqladm : DBAilfreight1!`.
9. **Targeted Kerberoasting**: Injected fake SPN (`acmetesting/LEGIT`) onto `ttimmons` using `mssqladm`'s `GenericWrite` rights; requested TGS and cracked password `Repeat09` via Hashcat.
10. **Privileged Group Self-Addition**: Exploited `ttimmons`'s `GenericAll` control over custom group `Server Admins` to add `ttimmons` into `Server Admins`.
11. **DCSync Attack (Domain Compromise)**: Exploited `Server Admins` extended replication rights (`GetChanges`/`GetChangesAll`) via `secretsdump.py` to dump all domain hashes (`Administrator` NTLM hash: `fd1f7e5564060258ea787ddbb6e6afa2`).
12. **Proof of Domain Compromise**: Pass-the-Hash authentication via `evil-winrm` as `Administrator` on Domain Controller DC01.

---

## How to Run & Verify

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mazonia/privilege-escalation-n-dom-compromise.git
   cd privilege-escalation-n-dom-compromise
   ```

2. **Inspect the Full Written Report**:
   - Open [`docs/INLANEFREIGHT_AD_Compromise_Report.pdf`](docs/INLANEFREIGHT_AD_Compromise_Report.pdf) or [`docs/INLANEFREIGHT_AD_Compromise_Report.docx`](docs/INLANEFREIGHT_AD_Compromise_Report.docx).

3. **Review Execution Commands**:
   - View complete syntax in [`scripts/attack_chain_playbook.sh`](scripts/attack_chain_playbook.sh).

---

## Disclaimer & Academic Integrity

This project was conducted strictly inside an isolated, instructor-approved university laboratory environment for academic evaluation in course **CY376**. All testing was performed against consenting systems. No weaponized exploits or real-world target data are contained within this repository.
