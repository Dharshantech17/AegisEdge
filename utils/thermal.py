"""
Hardware Health & Thermal Management Engine for Arm Cortex-A (Raspberry Pi 4 / 5).
Monitors SoC temperature via sysfs to ensure sustained high throughput without thermal throttling.
"""

import os
import platform

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class EdgeHardwareMonitor:
    def __init__(self, throttle_temp_celsius=75.0):
        self.throttle_temp = throttle_temp_celsius
        self.is_linux = platform.system().lower() == "linux"
        self.thermal_path = "/sys/class/thermal/thermal_zone0/temp"

    def get_soc_temperature(self):
        """Returns CPU temperature in Celsius (or simulated/mock on non-Linux host)."""
        if self.is_linux and os.path.exists(self.thermal_path):
            try:
                with open(self.thermal_path, "r") as f:
                    temp_raw = f.read().strip()
                return round(float(temp_raw) / 1000.0, 1)
            except Exception:
                pass
        return 42.5  # Nominal fallback for development / host PCs

    def get_system_telemetry(self):
        """Returns snapshot of CPU, RAM, and thermal state."""
        temp = self.get_soc_temperature()
        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            cpu_pct = psutil.cpu_percent(interval=None)
            ram_used = round((mem.total - mem.available) / (1024 * 1024), 1)
            ram_pct = mem.percent
        else:
            cpu_pct = 25.0
            ram_used = 165.0
            ram_pct = 20.0

        return {
            "soc_temp_celsius": temp,
            "is_thermal_warning": temp >= self.throttle_temp,
            "cpu_utilization_pct": cpu_pct,
            "ram_used_mb": ram_used,
            "ram_utilization_pct": ram_pct
        }
