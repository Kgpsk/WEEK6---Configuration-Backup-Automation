from netmiko import ConnectHandler, redispatch
import time
from datetime import datetime
import os

# Create backup folder with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_folder = f"backups_{timestamp}"
os.makedirs(backup_folder, exist_ok=True)
print(f"[📁] Backup folder created: {backup_folder}")

# R1 connection details (reachable from PC)
r1 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.53",
    "username": "admin",
    "password": "admin",
    "secret": "admin",
    "global_delay_factor": 2,
}

# All routers with their connection info
routers = [
    {"name": "R1", "ip": "192.168.122.53", "reachable": True},
    {"name": "R2", "ip": "10.10.10.2", "reachable": False},
    {"name": "R3", "ip": "10.10.30.2", "reachable": False},
]

print("\n" + "=" * 60)
print("CONFIGURATION BACKUP AUTOMATION")
print("=" * 60)
print(f"[🔹] Total routers: {len(routers)}")
print(f"[🔹] Backup folder: {backup_folder}")
print("=" * 60)

# Connect to R1
print("\n[1] Connecting to R1...")
connection = ConnectHandler(**r1)
connection.enable()
print(f"✅ Connected to R1 ({r1['host']})")

# Backup R1 config
print("\n[2] Backing up R1 configuration...")
output = connection.send_command("show running-config")
filename = f"{backup_folder}/R1_running-config.txt"
with open(filename, "w") as f:
    f.write(output)
print(f"✅ R1 backup saved to {filename}")

# === SSH to R2 via R1 ===
print("\n[3] SSH from R1 to R2...")
connection.write_channel("ssh -l admin 10.10.10.2\n")
time.sleep(2)
connection.write_channel("admin\n")
time.sleep(2)
connection.read_channel()
redispatch(connection, device_type="cisco_ios")
time.sleep(1)

print("[4] Entering enable mode on R2...")
connection.write_channel("enable\n")
time.sleep(1)
connection.write_channel("admin\n")
time.sleep(2)

print("\n[5] Backing up R2 configuration...")
connection.write_channel("show running-config\n")
time.sleep(3)
output = connection.read_channel()
filename = f"{backup_folder}/R2_running-config.txt"
with open(filename, "w") as f:
    f.write(output)
print(f"✅ R2 backup saved to {filename}")

# === SSH to R3 via R2 ===
print("\n[6] SSH from R2 to R3...")
connection.write_channel("ssh -l admin 10.10.30.2\n")
time.sleep(2)
connection.write_channel("admin\n")
time.sleep(2)
connection.read_channel()
redispatch(connection, device_type="cisco_ios")
time.sleep(1)

print("[7] Entering enable mode on R3...")
connection.write_channel("enable\n")
time.sleep(1)
connection.write_channel("admin\n")
time.sleep(2)

print("\n[8] Backing up R3 configuration...")
connection.write_channel("show running-config\n")
time.sleep(3)
output = connection.read_channel()
filename = f"{backup_folder}/R3_running-config.txt"
with open(filename, "w") as f:
    f.write(output)
print(f"✅ R3 backup saved to {filename}")

# Disconnect
connection.disconnect()
print("\n" + "=" * 60)
print("BACKUP COMPLETE!")
print("=" * 60)
print(f"\n✅ All configurations backed up to: {backup_folder}")
print("\nFiles created:")
for file in os.listdir(backup_folder):
    print(f"   - {file}")

print("\n📁 Backup location:")
print(f"   /home/kushan/Desktop/network task/week6/{backup_folder}")
