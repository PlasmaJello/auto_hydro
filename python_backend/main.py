import time
from datetime import datetime

class AutomatedHydroponics:
    def __init__(self, crop_type="leafy_greens"):
        # Configuration based on crop type
        self.crop_settings = {
            "leafy_greens": {"target_ph": 6.0, "target_ec": 1.2, "light_hours": 16},
            "tomatoes": {"target_ph": 6.2, "target_ec": 2.5, "light_hours": 14}
        }
        self.settings = self.crop_settings.get(crop_type)
        if self.settings is None:
            valid_crops = ", ".join(self.crop_settings.keys())
            raise ValueError(f"Unsupported crop_type: '{crop_type}'. Please choose from: {valid_crops}")
            
        self.pump_interval = 1800  # Flood every 30 mins
        self.flood_duration = 600  # Stay flooded for 10 mins
        self.ph_tolerance = 0.2
        self.ec_tolerance = 0.5

    def monitor_and_adjust(self):
        """Main loop to simulate sensor reading and robotic adjustment."""
        while True:
            current_ph = self.read_sensor("PH")
            current_ec = self.read_sensor("EC")
            
            self.adjust_ph(current_ph)
            self.adjust_ec(current_ec)
            self.manage_lighting()
            self.manage_ebb_and_flow()
            
            time.sleep(60)

    def adjust_ph(self, current_ph):
        """Robotic adjustment for acidity/alkalinity."""
        target = self.settings["target_ph"]
        if current_ph > target + self.ph_tolerance:
            self.robot_command("DISPENSE_PH_DOWN")
        elif current_ph < target - self.ph_tolerance:
            self.robot_command("DISPENSE_PH_UP")

    def adjust_ec(self, current_ec):
        """Robotic adjustment for Electrical Conductivity (Nutrient strength)."""
        target = self.settings["target_ec"]
        if current_ec < target:
            self.robot_command("INJECT_NUTRIENT_CONCENTRATE")
        elif current_ec > target + self.ec_tolerance:
            self.robot_command("ADD_FRESH_WATER_DILUTION")

    def manage_lighting(self):
        """Adjusts light cycle based on crop requirements."""
        current_hour = datetime.now().hour
        if 0 <= current_hour < self.settings["light_hours"]:
            self.robot_command("LIGHTS_ON")
        else:
            self.robot_command("LIGHTS_OFF")

    def manage_ebb_and_flow(self):
        """Controls the pump for the Ebb and Flow mechanism."""
        # Logic: Flood the tray at specific intervals
        current_seconds = int(time.time()) % self.pump_interval
        if current_seconds < self.flood_duration:
            self.robot_command("PUMP_ON_FLOODING")
        else:
            self.robot_command("PUMP_OFF_DRAINING")

    def read_sensor(self, sensor_type):
        """Placeholder for actual hardware sensor integration."""
        # In a real system, this would interface with I2C/Analog probes
        return 6.0 if sensor_type == "PH" else 1.2

    def robot_command(self, action):
        """Sends instructions to the mechanical adjusting mechanisms."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ROBOT EXECUTION: {action}")

if __name__ == "__main__":
    # Initialize system for tomatoes
    system = AutomatedHydroponics(crop_type="tomatoes")
    print("Starting Automated Ebb and Flow System...")
    try:
        system.monitor_and_adjust()
    except KeyboardInterrupt:
        print("System Shutdown.")
```