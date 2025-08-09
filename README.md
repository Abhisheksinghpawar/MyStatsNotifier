📘  — Real-Time Desktop & Network Performance Monitor

A lightweight Python tool for monitoring system performance and network health with smart alerts and desktop notifications.

🚀 Features

🖥️ System Monitoring
  
    • 	Real-time CPU, RAM, and Disk usage
  
    • 	Threshold-based alerts (e.g. CPU > 5%)

🌐 Network Monitoring
  
    • 	Bandwidth stats (bytes sent/received)
  
    • 	Ping test with latency and packet loss detection

🔔 Smart Notifications
  
    •  Desktop alerts every 100 seconds
  
    • 	Immediate alerts if CPU crosses threshold
  
    • 	Emoji-enhanced summaries for clarity

🎨 Terminal UI
 
    • 	Colour-coded output using 
 
    • 	Tabular display with 
  
  • 	Icons and formatting for readability

⚙️ Modular Design
  
  • 	Easy to extend with CLI flags, logging, or AI summaries
 
  • 	Clean separation of logic for system, network, and alerts

📦 Installation
  
    pip install psutil plyer colorama tabulate

▶️ Usage
 
    • 	Alerts every 100 seconds
 
    • 	Immediate alert if CPU usage exceeds 5%
  
    • 	Ping target:  (default)

📈 Future Scope
Here’s what’s planned next:
  
    • 	🧠 Anomaly Detection: Rolling averages and spike detection
 
    • 	📊 Logging: Export stats to CSV or SQLite for trend analysis
 
    • 	🛠️ CLI Flags: Custom interval, ping host, silent mode
 
    • 	🔗 Webhook/Slack Alerts: Push alerts to remote dashboards
 
    • 	🧪 Process-Level Stats: Show top CPU/memory-consuming processes
 
    • 	🔋 Battery & Power Monitoring: Add battery %, charging status
 
    • 	🧠 AI Summary Mode: Natural language summaries via Ollama or LLM

🤝 Contributing
      Pull requests and feature suggestions are welcome! If you’ve got ideas for integrations, UI enhancements, or smarter alerting—let’s build it together.
