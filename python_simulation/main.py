import os
import time
import random
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# --- CONFIGURATION ---
VOLTAGE = 230.0  # Constant grid voltage (Volts)
HIGH_POWER_THRESHOLD = 2500.0  # Alert threshold (Watts)
TARIFF_PER_KWH = 0.15  # Electricity cost rate ($)
DATA_FILE = "data/energy_logs.csv"

# Ensure output directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

class EnergyMonitor:
    def __init__(self):
        self.total_energy_kwh = 0.0
        self.init_csv()

    def init_csv(self):
        """Initializes the CSV log file with structural headers [12]."""
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Voltage(V)", "Current(A)", "Power(W)", "Energy(kWh)", "Cost($)", "Alert Status"])

    def simulate_appliance_current(self):
        """Simulates realistic household electrical loads [11]."""
        modes = [
            ("Normal (LEDs + Laptop)", random.uniform(0.5, 2.0)),
            ("Medium (Fridge + TV)", random.uniform(2.5, 6.0)),
            ("Heavy (AC / Microwave)", random.uniform(11.0, 15.0)),
            ("Overload Spike", random.uniform(16.0, 22.0))
        ]
        mode_name, current = random.choices(modes, weights=[50, 35, 12, 3], k=1)[0]
        return round(current, 2), mode_name

    def calculate_metrics(self, current, time_interval_sec=2):
        """Computes true electrical power, cumulative energy, and financial cost [5, 6]."""
        power_w = VOLTAGE * current
        
        # Energy (kWh) = (Power in Watts * Time in Hours) / 1000
        time_hours = time_interval_sec / 3600.0
        energy_interval_kwh = (power_w * time_hours) / 1000.0
        self.total_energy_kwh += energy_interval_kwh
        
        cost = self.total_energy_kwh * TARIFF_PER_KWH
        
        # Alert Engine Evaluation [5, 8]
        alert_status = "CRITICAL: OVERLOAD" if power_w > HIGH_POWER_THRESHOLD else "NORMAL"
        
        return round(power_w, 2), round(self.total_energy_kwh, 6), round(cost, 4), alert_status

    def log_to_csv(self, timestamp, current, power_w, energy_kwh, cost, alert):
        """Appends raw engine data straight to the data ledger [12]."""
        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, VOLTAGE, current, power_w, energy_kwh, cost, alert])

    def generate_analytics_report(self):
        """Compiles analytical visual charts and a compiled PDF report [12]."""
        print("\n📊 Compiling system data and generating PDF report...")
        df = pd.read_csv(DATA_FILE)
        if df.empty: return

        # 1. Generate & Save Dashboard Analytical Chart
        plt.figure(figsize=(10, 5))
        plt.plot(pd.to_datetime(df['Timestamp']), df['Power(W)'], color='orange', label='Power Demand (W)')
        plt.axhline(y=HIGH_POWER_THRESHOLD, color='red', linestyle='--', label='Overload Limit')
        plt.title('Real-Time Power Demand Analytics')
        plt.xlabel('Timeline')
        plt.ylabel('Power (Watts)')
        plt.legend()
        plt.gcf().autofmt_xdate()
        chart_path = "outputs/power_chart.png"
        plt.savefig(chart_path)
        plt.close()

        # 2. Build Industrial PDF Compliance Summary Report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, "Smart Home Energy Audit Report", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", size=11)
        pdf.cell(190, 10, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.cell(190, 10, f"Total Data Samples Processed: {len(df)}", ln=True)
        pdf.cell(190, 10, f"Peak Demand Registered: {df['Power(W)'].max()} W", ln=True)
        pdf.cell(190, 10, f"Total Accumulated Consumption: {round(df['Energy(kWh)'].iloc[-1], 4)} kWh", ln=True)
        pdf.cell(190, 10, f"Calculated Financial Cost: ${round(df['Cost($)'].iloc[-1], 2)}", ln=True)
        pdf.ln(10)
        
        # Append visual analytics directly inside document canvas
        pdf.image(chart_path, x=10, y=70, w=190)
        
        pdf.output("outputs/Energy_Audit_Report.pdf")
        print("✅ Success! Check 'outputs/Energy_Audit_Report.pdf' and 'outputs/power_chart.png'!")

# --- EXECUTION LOOP ---
if __name__ == "__main__":
    monitor = EnergyMonitor()
    print("⚡ Smart Home Energy Simulation Engine Active [Press Ctrl+C to terminate] ⚡")
    print("-------------------------------------------------------------------------")
    
    ticks = 0
    try:
        # Run for 15 iterations to generate sample data
        while ticks < 15:
            current, mode = monitor.simulate_appliance_current()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            power, energy, cost, alert = monitor.calculate_metrics(current)
            
            monitor.log_to_csv(timestamp, current, power, energy, cost, alert)
            
            print(f"[{timestamp}] Load Mode: {mode}")
            print(f" └─ Metrics -> Current: {current}A | Power: {power}W | Energy: {energy}kWh | Cost: ${cost}")
            if alert != "NORMAL":
                print(f" 🚨 ALERT: High Power Draw Registered!")
            print("-" * 75)
            
            time.sleep(1)
            ticks += 1
            
        # Compile asset pipeline data into visual artifacts
        monitor.generate_analytics_report()

    except KeyboardInterrupt:
        monitor.generate_analytics_report()
        print("\nSimulation shut down gracefully.")
