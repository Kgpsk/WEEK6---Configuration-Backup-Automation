# Week 6: Configuration Backup Automation

**Date:** August 2026  
**Topic:** Automating Router Configuration Backups with Python  
**Target:** Network Automation Engineer  

---

## Project Overview

This project automates the backup of running configurations from multiple Cisco routers using Python and Netmiko. The script connects to each router, retrieves the running configuration, and saves it to a timestamped file.

Only the edge router (R1) is directly reachable. Internal routers (R2 and R3) are accessed through SSH hopping.

---

## Topology


Internet (Cloud)
|
|
R1 (Edge Router) ---- R2 (Internal Router) ---- R3 (Database Router)
192.168.122.53 10.10.10.2 10.10.30.2


---

## Device Details

| Device | Interface | IP Address | Role |
|--------|-----------|------------|------|
| R1 | FastEthernet 0/0 | 10.10.10.1/30 | Edge Router |
| R1 | FastEthernet 0/1 | 192.168.122.53/24 | Cloud/Internet |
| R2 | FastEthernet 0/0 | 10.10.10.2/30 | Internal Router |
| R2 | FastEthernet 0/1 | 10.10.30.1/30 | Internal Router |
| R3 | FastEthernet 0/0 | 10.10.30.2/30 | Database Router |

---

## Router Configurations

### R1 (Edge Router)


enable
configure terminal
hostname R1
interface fastEthernet 0/0
ip address 10.10.10.1 255.255.255.252
no shutdown
exit
interface fastEthernet 0/1
ip address dhcp
no shutdown
exit
ip domain-name lab.local
crypto key generate rsa
1024
username admin password admin
enable secret admin
line vty 0 4
login local
transport input ssh
exit
end
write memory


### R2 (Internal Router)

enable
configure terminal
hostname R2
interface fastEthernet 0/0
ip address 10.10.10.2 255.255.255.252
no shutdown
exit
interface fastEthernet 0/1
ip address 10.10.30.1 255.255.255.252
no shutdown
exit
ip domain-name lab.local
crypto key generate rsa
1024
username admin password admin
enable secret admin
line vty 0 4
login local
transport input ssh
exit
end
write memory


### R3 (Database Router)


enable
configure terminal
hostname R3
interface fastEthernet 0/0
ip address 10.10.30.2 255.255.255.252
no shutdown
exit
ip domain-name lab.local
crypto key generate rsa
1024
username admin password admin
enable secret admin
line vty 0 4
login local
transport input ssh
exit
end
write memory


---

## Python Script: backup_configs.py

### What the Script Does

1. Creates a timestamped backup folder
2. Connects to R1 (reachable from PC)
3. Backs up R1 running-config
4. SSHs from R1 to R2 using write_channel
5. Backs up R2 running-config
6. SSHs from R2 to R3 using write_channel
7. Backs up R3 running-config
8. Displays all created files

### Key Functions Used

| Function | Purpose |
|----------|---------|
| `datetime.now().strftime()` | Creates timestamp for folder name |
| `os.makedirs()` | Creates backup folder |
| `ConnectHandler()` | SSH to device |
| `connection.enable()` | Enter enable mode |
| `send_command("show running-config")` | Retrieves full configuration |
| `write_channel()` | Send raw SSH commands |
| `read_channel()` | Read output buffer |
| `redispatch()` | Change device context |
| `with open(filename, "w") as f:` | Writes config to file |

---

## Script Output


[📁] Backup folder created: backups_2026-08-12_02-45-12

============================================================
CONFIGURATION BACKUP AUTOMATION
============================================================
[🔹] Total routers: 3
[🔹] Backup folder: backups_2026-08-12_02-45-12
============================================================

[1] Connecting to R1...
✅ Connected to R1 (192.168.122.53)

[2] Backing up R1 configuration...
✅ R1 backup saved to backups_2026-08-12_02-45-12/R1_running-config.txt

[3] SSH from R1 to R2...
[4] Entering enable mode on R2...

[5] Backing up R2 configuration...
✅ R2 backup saved to backups_2026-08-12_02-45-12/R2_running-config.txt

[6] SSH from R2 to R3...
[7] Entering enable mode on R3...

[8] Backing up R3 configuration...
✅ R3 backup saved to backups_2026-08-12_02-45-12/R3_running-config.txt

============================================================
BACKUP COMPLETE!
============================================================

✅ All configurations backed up to: backups_2026-08-12_02-45-12

Files created:

    R1_running-config.txt

    R2_running-config.txt

    R3_running-config.txt

📁 Backup location:
backups_2026-08-12_02-45-12



---

## Backup File Structure


📁 backups_2026-08-12_02-45-12/
├── R1_running-config.txt (1039 bytes)
├── R2_running-config.txt
└── R3_running-config.txt


---

## What I Learned

| # | Learning |
|---|----------|
| 1 | Configuration backups are essential for disaster recovery |
| 2 | Timestamped folders organize backups chronologically |
| 3 | datetime.now().strftime() creates formatted timestamps |
| 4 | os.makedirs() creates folders programmatically |
| 5 | with open(filename, "w") as f: writes files in Python |
| 6 | send_command("show running-config") retrieves the entire config |
| 7 | SSH hopping works for backups too |
| 8 | Backups can be automated across multiple devices |

---

## Real-World Applications

| Scenario | Description |
|----------|-------------|
| **Routine Backups** | Schedule daily backups of all network devices |
| **Change Management** | Backup before and after changes to compare |
| **Disaster Recovery** | Restore configurations instantly after failure |
| **Audit & Compliance** | Maintain historical records of network changes |
| **Migration** | Backup old devices before replacement |
| **Version Control** | Track configuration changes over time |

---

## Project Files

| File | Description |
|------|-------------|
| `backup_configs.py` | Main Python script |
| `README.md` | This file |
| Screenshots/ | GNS3 topology and backup folder |

---

## Next Steps

- [ ] Week 7: Network Monitoring with Python
- [ ] Week 8: Final Project + Portfolio

---

## Quote

> "An unbacked configuration is a disaster waiting to happen."

---

**END OF README**
