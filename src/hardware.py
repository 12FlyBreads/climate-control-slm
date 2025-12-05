# === hardware.py ===

# Libraries
import board
import adafruit_dht
import adafruit_bmp280
from gpiozero import LED, Button
import time
from utils import load_config

# Global Configuration Load
CONFIG = load_config()
HARDWARE = CONFIG['hardware_config']

# --- Hardware Configuration and Initialization ---
# DHT22 Sensor
DHT22Sensor = adafruit_dht.DHT22(getattr(board, f"D{HARDWARE['dht_data_pin']}")) 

# BMP280 Sensor
i2c = board.I2C()
bmp280Sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=HARDWARE['bmp280_i2c_address'])
bmp280Sensor.sea_level_pressure = HARDWARE['sea_level_pressure']

# Actuators (LEDs simulate Fan/Heater/Status)
ledRed = LED(HARDWARE['led_red_pin'])
ledYlw = LED(HARDWARE['led_yellow_pin'])
ledGrn = LED(HARDWARE['led_green_pin'])

# Input
button = Button(HARDWARE['button_pin'])

# --- Functions for Data Collection ---
def read_environment_data():
    """
    Reads temperature, humidity, pressure, and button state.
    Returns a dictionary with all environmental data.
    """
    try:
        data = {
            "dht_temperature_c": DHT22Sensor.temperature,
            "humidity_percent": DHT22Sensor.humidity,
            "bmp_temperature_c": bmp280Sensor.temperature,
            "pressure_hpa": bmp280Sensor.pressure,
            "button_pressed": button.is_pressed
        }
        
        if any(v is None for k, v in data.items() if not k.startswith('button')):
            raise RuntimeError("Some sensor data is unavailable (None).")
            
        for key in ['dht_temperature_c', 'humidity_percent', 'bmp_temperature_c']:
            data[key] = round(data[key], 1)
        data['pressure_hpa'] = round(data['pressure_hpa'], 2)
        
        return data
        
    except RuntimeError as e:
        print(f"Sensor read error: {e}")
        time.sleep(1)
        return {"error": str(e)}
        
# --- Functions for Actuator Control ---
def set_led_state(color: str, state: str) -> str:
    """
    Turns a specific LED on or off (simulating actuators).
    Args:
        color (str): The color of the LED ('red', 'yellow', 'green').
        state (str): The desired state ('on', 'off').
    Returns:
        str: A confirmation message.
    """
    led_map = {
        'red': ledRed,
        'yellow': ledYlw,
        'green': ledGrn
    }
    
    if color.lower() not in led_map:
        return f"Error: Invalid LED color '{color}'."
        
    led = led_map[color.lower()]
    state_lower = state.lower()
    
    if state_lower == 'on':
        led.on()
        return f"LED {color.upper()} turned on successfully."
    elif state_lower == 'off':
        led.off()
        return f"LED {color.upper()} turned off successfully."
    else:
        return f"Error: Invalid state '{state}'. Use 'on' or 'off'."

def get_led_status() -> dict:
    """
    Returns the current state of all LEDs.
    """
    return {
        "red_led_status": "on" if ledRed.is_lit else "off",
        "yellow_led_status": "on" if ledYlw.is_lit else "off",
        "green_led_status": "on" if ledGrn.is_lit else "off"
    }