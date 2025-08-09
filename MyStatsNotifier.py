import psutil
import time
import subprocess
from plyer import notification
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

# 🔧 Thresholds for alerts
THRESHOLDS = {
    "CPU": 85,
    "RAM": 85,
    "Disk": 90,
    "PacketLoss": 0  # Any packet loss triggers alert
}

# 🖥️ System stats
def get_system_stats():
    return {
        "CPU (%)": psutil.cpu_percent(interval=1),
        "RAM (%)": psutil.virtual_memory().percent,
        "Disk (%)": psutil.disk_usage('/').percent
    }

# 🌐 Network stats
def get_network_stats():
    net_io = psutil.net_io_counters()
    return {
        "Bytes Sent": f"{net_io.bytes_sent / (1024 ** 2):.2f} MB",
        "Bytes Received": f"{net_io.bytes_recv / (1024 ** 2):.2f} MB"
    }

# 📶 Ping test with latency + packet loss
def ping_test(host="8.8.8.8", count=4):
    try:
        output = subprocess.check_output(["ping", host, "-n", str(count)], universal_newlines=True)
        lines = output.splitlines()
        stats_line = next((line for line in lines if "Minimum" in line), None)
        loss_line = next((line for line in lines if "Lost" in line), None)

        # Parse latency
        if stats_line:
            parts = stats_line.split(",")
            min_val = parts[0].split("=")[1].strip()
            max_val = parts[1].split("=")[1].strip()
            avg_val = parts[2].split("=")[1].strip()
        else:
            min_val = max_val = avg_val = "N/A"

        # Parse packet loss
        if loss_line:
            loss_percent = loss_line.split(",")[-1].split("=")[-1].strip()
        else:
            loss_percent = "N/A"

        return {
            "Min": min_val,
            "Max": max_val,
            "Avg": avg_val,
            "Loss": loss_percent
        }
    except subprocess.CalledProcessError:
        return {"Min": "N/A", "Max": "N/A", "Avg": "N/A", "Loss": "100%"}

# 🚨 Alert logic
def should_alert(sys_stats, ping_stats):
    if sys_stats["CPU (%)"] > THRESHOLDS["CPU"]:
        return True
    if sys_stats["RAM (%)"] > THRESHOLDS["RAM"]:
        return True
    if sys_stats["Disk (%)"] > THRESHOLDS["Disk"]:
        return True
    try:
        loss = int(ping_stats["Loss"].replace("%", ""))
        if loss > THRESHOLDS["PacketLoss"]:
            return True
    except:
        return True  # If parsing fails, assume alert
    return False

# 🎨 Notification formatter
def format_notification(sys_stats, net_stats, ping_stats):
    return (
        f"🖥️ CPU: {sys_stats['CPU (%)']}% | RAM: {sys_stats['RAM (%)']}% | Disk: {sys_stats['Disk (%)']}%\n"
        f"🌐 Sent: {net_stats['Bytes Sent']} | Received: {net_stats['Bytes Received']}\n"
        f"📶 Ping: Min {ping_stats['Min']} | Max {ping_stats['Max']} | Avg {ping_stats['Avg']} | Loss: {ping_stats['Loss']}"
    )

# 🔔 Desktop notification
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5  # seconds
    )

# 🖥️ Terminal display + conditional alert
def display_stats():
    sys_stats = get_system_stats()
    net_stats = get_network_stats()
    ping_stats = ping_test()

    # Terminal output
    table_data = [
        ["CPU Usage", sys_stats["CPU (%)"]],
        ["RAM Usage", sys_stats["RAM (%)"]],
        ["Disk Usage", sys_stats["Disk (%)"]],
        ["Bytes Sent", net_stats["Bytes Sent"]],
        ["Bytes Received", net_stats["Bytes Received"]],
        ["Ping", f"Min {ping_stats['Min']} | Max {ping_stats['Max']} | Avg {ping_stats['Avg']} | Loss: {ping_stats['Loss']}"]
    ]
    #print(Style.BRIGHT + tabulate(table_data, headers=["Metric", "Value"], tablefmt="fancy_grid"))

    # Conditional notification
    if should_alert(sys_stats, ping_stats):
        notif_msg = format_notification(sys_stats, net_stats, ping_stats)
        send_notification("⚠️ PerfNetMonitor Alert", notif_msg)

# 🔁 Main loop
if __name__ == "__main__":
    last_notified = 0
    notify_interval = 1800  # seconds

    while True:
        #print("\n🖥️ System & 🌐 Network Monitor")
        sys_stats = get_system_stats()
        net_stats = get_network_stats()
        ping_stats = ping_test()

        # Terminal output
        table_data = [
            ["CPU Usage", sys_stats["CPU (%)"]],
            ["RAM Usage", sys_stats["RAM (%)"]],
            ["Disk Usage", sys_stats["Disk (%)"]],
            ["Bytes Sent", net_stats["Bytes Sent"]],
            ["Bytes Received", net_stats["Bytes Received"]],
            ["Ping", f"Min {ping_stats['Min']} | Max {ping_stats['Max']} | Avg {ping_stats['Avg']} | Loss: {ping_stats['Loss']}"]
        ]
        #print(Style.BRIGHT + tabulate(table_data, headers=["Metric", "Value"], tablefmt="fancy_grid"))

        # Notification logic
        current_time = time.time()
        cpu_triggered = sys_stats["CPU (%)"] > THRESHOLDS["CPU"]
        time_triggered = (current_time - last_notified) >= notify_interval

        if cpu_triggered or time_triggered:
            notif_msg = format_notification(sys_stats, net_stats, ping_stats)
            title = "⚠️ High CPU Alert" if cpu_triggered else "📊 PerfNetMonitor Update"
            send_notification(title, notif_msg)
            last_notified = current_time

        time.sleep(10)