WEEK 6: CONFIGURATION BACKUP AUTOMATION REPORT
DATE: August 2026
TOPIC: Automating Router Configuration Backups with Python and Netmiko
OBJECTIVE: Automatically backup running configurations from multiple routers


1. PROJECT OVERVIEW

This project automated the backup of running configurations from three Cisco routers using Python and Netmiko. The script connects to each router, retrieves the running configuration, and saves it to a timestamped file.

The topology uses a real-world enterprise design where only the edge router (R1) is directly reachable from the PC. Internal routers (R2 and R3) are accessed through SSH hopping.


2. TOPOLOGY

Internet (Cloud)
    |
    |
R1 (Edge Router) ---- R2 (Internal Router) ---- R3 (Database Router)
192.168.122.53         10.10.10.2               10.10.30.2


3. DEVICE DETAILS

| Device | Interface | IP Address | Role |
|--------|-----------|------------|------|
| R1 | FastEthernet 0/0 | 10.10.10.1/30 | Edge Router |
| R1 | FastEthernet 0/1 | 192.168.122.53/24 | Cloud/Internet |
| R2 | FastEthernet 0/0 | 10.10.10.2/30 | Internal Router |
| R2 | FastEthernet 0/1 | 10.10.30.1/30 | Internal Router |
| R3 | FastEthernet 0/0 | 10.10.30.2/30 | Database Router |


4. ROUTER CONFIGURATIONS

R1 (Edge Router):
- Hostname: R1
- FastEthernet 0/0: 10.10.10.1/30
- FastEthernet 0/1: DHCP (192.168.122.53)
- SSH enabled with username admin password admin
- Enable secret: admin

R2 (Internal Router):
- Hostname: R2
- FastEthernet 0/0: 10.10.10.2/30
- FastEthernet 0/1: 10.10.30.1/30
- SSH enabled with username admin password admin
- Enable secret: admin

R3 (Database Router):
- Hostname: R3
- FastEthernet 0/0: 10.10.30.2/30
- SSH enabled with username admin password admin
- Enable secret: admin


5. PYTHON SCRIPT: backup_configs.py

Key Components:

from datetime import datetime
import os

# Create timestamped folder
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_folder = f"backups_{timestamp}"
os.makedirs(backup_folder, exist_ok=True)

# Backup R1
output = connection.send_command("show running-config")
filename = f"{backup_folder}/R1_running-config.txt"
with open(filename, "w") as f:
    f.write(output)

# SSH hopping for R2 and R3 using write_channel and redispatch


6. SCRIPT OUTPUT

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
   - R1_running-config.txt
   - R2_running-config.txt
   - R3_running-config.txt

📁 Backup location:
   /home/kushan/Desktop/network task/week6/backups_2026-08-12_02-45-12


7. BACKUP FILE STRUCTURE

📁 backups_2026-08-12_02-45-12/
├── R1_running-config.txt  (1039 bytes)
├── R2_running-config.txt
└── R3_running-config.txt

R1_running-config.txt Content Includes:
- Hostname: R1
- Enable secret
- Username: admin
- SSH transport
- FastEthernet 0/0 IP: 10.10.10.1/30
- FastEthernet 0/1 IP: DHCP
- Domain name: lab.local


8. COMMANDS USED IN THE SCRIPT

| Python Code | Purpose |
|-------------|---------|
| from datetime import datetime | Import timestamp functionality |
| datetime.now().strftime("%Y-%m-%d_%H-%M-%S") | Creates timestamp string |
| os.makedirs(folder, exist_ok=True) | Creates folder if it doesn't exist |
| connection.send_command("show running-config") | Gets full router config |
| with open(filename, "w") as f: | Opens file for writing |
| f.write(output) | Writes config to file |
| connection.write_channel() | Send raw SSH commands |
| connection.read_channel() | Read output buffer |
| redispatch() | Change device context |
| time.sleep() | Add delays for stability |


9. ERRORS ENCOUNTERED AND FIXES

| # | Error | Cause | Fix |
|---|-------|-------|-----|
| 1 | File not found | Folder didn't exist | Used os.makedirs() to create folder |
| 2 | SSH timeout | R2 not reachable from PC | Used SSH hopping via R1 |
| 3 | No password set on R3 | Enable secret not configured | Configured enable secret admin on R3 |
| 4 | OSPF commands failed | R3 not in enable mode | Manually sent enable and password |


10. WHAT I LEARNED

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
| 9 | File handling is a critical skill for automation |
| 10 | Timestamps help identify when backups were taken |


11. REAL-WORLD APPLICATIONS

| Scenario | Description |
|----------|-------------|
| Routine Backups | Schedule daily backups of all network devices |
| Change Management | Backup before and after changes to compare |
| Disaster Recovery | Restore configurations instantly after failure |
| Audit & Compliance | Maintain historical records of network changes |
| Migration | Backup old devices before replacement |
| Version Control | Track configuration changes over time |
| Incident Response | Compare current config with last known good backup |


12. NEXT STEPS

- [ ] Week 7: Network Monitoring with Python
- [ ] Week 8: Final Project + Portfolio


13. CONCLUSION

This project successfully demonstrated automated configuration backups across multiple routers using Python and Netmiko. The script creates timestamped backups, connects to each router through SSH hopping, and saves the running configurations to organized files.

This is a practical skill that every network engineer needs for disaster recovery, change management, and compliance.

---

END OF REPORT
