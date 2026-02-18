import os
import json
import platform
import socket
import subprocess
import requests
import psutil
from datetime import datetime


def get_system_info():
    """Gather comprehensive system information"""
    info = {}
    
    # Basic system info
    info["platform"] = platform.system()
    info["platform_release"] = platform.release()
    info["platform_version"] = platform.version()
    info["architecture"] = platform.machine()
    info["hostname"] = socket.gethostname()
    info["processor"] = platform.processor()
    
    # Network info
    try:
        info["ip_address"] = socket.gethostbyname(socket.gethostname())
    except:
        info["ip_address"] = "Unknown"
    
    # Memory info
    memory = psutil.virtual_memory()
    info["memory"] = {
        "total": f"{memory.total / (1024**3):.2f} GB",
        "available": f"{memory.available / (1024**3):.2f} GB",
        "used": f"{memory.used / (1024**3):.2f} GB",
        "percentage": f"{memory.percent}%"
    }
    
    # Disk info
    disk = psutil.disk_usage('/')
    info["disk"] = {
        "total": f"{disk.total / (1024**3):.2f} GB",
        "used": f"{disk.used / (1024**3):.2f} GB",
        "free": f"{disk.free / (1024**3):.2f} GB",
        "percentage": f"{(disk.used / disk.total) * 100:.1f}%"
    }
    
    # CPU info
    info["cpu_count"] = psutil.cpu_count()
    info["cpu_percent"] = f"{psutil.cpu_percent(interval=1)}%"
    
    # Boot time
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    info["boot_time"] = boot_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return info


def get_printer_info():
    """Get printer-specific information"""
    printer_info = {}
    
    # Path setup
    if os.name == "nt":
        basePath = os.getcwd()
        configPath = os.path.normpath(os.path.join(basePath, "..", "out", "config"))
        databasePath = os.path.normpath(os.path.join(basePath, "..", "out", "database"))
    else:
        configPath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "config"))
        databasePath = os.path.normpath(os.path.join("/home", "pi", "printer_data", "database"))
    
    printer_info["config_path"] = configPath
    printer_info["database_path"] = databasePath
    
    # Read G1.Conf for serial number
    g1_conf_path = os.path.join(databasePath, "G1.Conf")
    if os.path.exists(g1_conf_path):
        try:
            with open(g1_conf_path, "r") as f:
                g1_conf = json.load(f)
                printer_info["serial_number"] = g1_conf.get("serial_number", "Unknown")
                printer_info["file_hashes"] = {k: v for k, v in g1_conf.items() if k != "serial_number"}
        except Exception as e:
            printer_info["serial_number"] = f"Error reading G1.Conf: {e}"
            printer_info["file_hashes"] = {}
    else:
        printer_info["serial_number"] = "G1.Conf not found - system not initialized"
        printer_info["file_hashes"] = {}
    
    # Check for update file
    update_file_path = os.path.join(databasePath, "G1-Update.temp")
    if os.path.exists(update_file_path):
        try:
            with open(update_file_path, "r") as f:
                update_info = json.load(f)
                printer_info["update_status"] = update_info
        except Exception as e:
            printer_info["update_status"] = f"Error reading update file: {e}"
    else:
        printer_info["update_status"] = "No update file found"
    
    # List config files
    if os.path.exists(configPath):
        try:
            config_files = [f for f in os.listdir(configPath) if os.path.isfile(os.path.join(configPath, f))]
            printer_info["config_files"] = config_files
            printer_info["config_file_count"] = len(config_files)
        except Exception as e:
            printer_info["config_files"] = f"Error listing config files: {e}"
            printer_info["config_file_count"] = 0
    else:
        printer_info["config_files"] = "Config directory not found"
        printer_info["config_file_count"] = 0
    
    return printer_info


def get_moonraker_info():
    """Get Moonraker/Klipper information"""
    moonraker_info = {}
    
    try:
        # Try to get Moonraker status
        response = requests.get("http://localhost:7125/server/info", timeout=5)
        response.raise_for_status()
        data = response.json().get("result", {})
        
        moonraker_info["moonraker_connected"] = True
        moonraker_info["moonraker_version"] = data.get("moonraker_version", "Unknown")
        moonraker_info["klipper_version"] = data.get("klipper_version", "Unknown")
        moonraker_info["host_info"] = data.get("host_info", {})
        
        # Get update status
        update_response = requests.get("http://localhost:7125/machine/update/status", timeout=5)
        update_response.raise_for_status()
        update_data = update_response.json().get("result", {}).get("version_info", {})
        
        moonraker_info["component_versions"] = {}
        for name, info in update_data.items():
            moonraker_info["component_versions"][name] = {
                "local": info.get("version", "Unknown"),
                "remote": info.get("remote_version", "Unknown"),
                "needs_update": info.get("version") != info.get("remote_version")
            }
        
    except requests.RequestException as e:
        moonraker_info["moonraker_connected"] = False
        moonraker_info["error"] = str(e)
    
    return moonraker_info


def run():
    """Main function to gather all information"""
    print("[Info Script] Gathering system information...")
    
    all_info = {
        "timestamp": datetime.now().isoformat(),
        "system": get_system_info(),
        "printer": get_printer_info(),
        "moonraker": get_moonraker_info()
    }
    
    return all_info


# For test manual
if __name__ == "__main__":
    info = run()
    print(json.dumps(info, indent=2))
