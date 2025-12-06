# === main.py === 

# Libraries
import sys
import select
import time
import json
import ollama
from utils import load_config
from inference import slm_inference_with_tools, SYSTEM_MESSAGE
from hardware import get_led_status, read_environment_data, set_led_state, button
from typing import Dict, Any, List

# --- Configurations ---
CONFIG = load_config()
MODEL = CONFIG['slm_config']['model_name']
BUTTON_CHECK_INTERVAL = CONFIG['system_config']['check_interval_s']
MAX_HISTORY = CONFIG['slm_config']['max_history_length']

# Load the prompt template
PROMPT_TEMPLATE = CONFIG['control_config']['button_control_prompt']

def display_status_and_control_leds(last_response: Dict[str, Any]):
    """
    Displays the system status and metrics.
    """

    current_led_status = get_led_status()
    current_data = read_environment_data()
    
    print("\n" + "="*60)
    print("SYSTEM STATUS & SENSOR DATA")
    print("="*60)
    
    if "error" not in current_data:
        print(f"DHT22: {current_data['dht_temperature_c']}°C / {current_data['humidity_percent']}%")
        print(f"BMP280: {current_data['bmp_temperature_c']}°C / {current_data['pressure_hpa']}hPa")
        print(f"Button: {'PRESSED' if button.is_pressed else 'NOT PRESSED'}") 
    else:
        print(f"Error reading sensors: {current_data['error']}")
        
    print(f"\nLED Status:")
    print(f"  Red LED:    {current_led_status['red_led_status'].upper()}")
    print(f"  Yellow LED: {current_led_status['yellow_led_status'].upper()}")
    print(f"  Green LED:  {current_led_status['green_led_status'].upper()}")
    
    print("="*60)
    
    print(f"\n--- SLM Metrics ---")
    print(f"Total Duration: {(last_response['total_duration']/1e9):.2f} seconds")
    print(f"Eval Rate: {last_response.get('eval_count', 0) / (last_response.get('eval_duration', 1) / 1e9):.2f} tokens/s\n")


def preload_model(MODEL: str):
    """
    Pre-loads the SLM model into memory to avoid initial latency on the first inference.
    Args:
        MODEL (str): The model name to preload.
    """
    print(f"Pre-loading model {MODEL}...")
    try:
        ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": "hi"}],
            stream=False 
        )
        print(f"Model {MODEL} loaded successfully!")
        
    except Exception as e:
        print("------------------------------------------------------------")
        print(f"⚠️ WARNING: Could not pre-load the model {MODEL}.")
        print("Make sure Ollama is running on the Raspberry Pi 5 and the model is downloaded.")
        print(f"Error details: {e}")
        print("------------------------------------------------------------")
        print("The model will be loaded on the first interaction, causing initial latency.")


def handle_slm_interaction(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Centralized function to send messages to the SLM and process the response.
    Args:
        messages (List[Dict[str, str]]): The current message history.
    Returns:
        List[Dict[str, str]]: The updated message history including the SLM response.
    """

    print("Assistant: [Analyzing and Controlling...]")
    
    response = slm_inference_with_tools(messages, MODEL)
    
    assistant_content = response['message']['content']
    
    messages.append({"role": "assistant", "content": assistant_content})
    
    print(f"Assistant: {assistant_content}")
    
    display_status_and_control_leds(response)
    
    if len(messages) > 9:
        messages = [messages[0]] + messages[-8:]
        
    return messages


def interactive_mode(MODEL: str):
    """
    Runs the system in interactive mode with button detection.
    """
    
    print("\n" + "="*60)
    print("INTELLIGENT CLIMATE CONTROL SYSTEM")
    print(f"Model: {MODEL}")
    print("="*60)
    print("Input Modes: 1. Terminal (Type a command) | 2. Button (Press for automatic control)\n")
    
    preload_model(MODEL)
    
    # Initialize the conversation with the system message
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_MESSAGE}
    ]
    
    # Stores the last button state to detect the falling edge (pressed -> released)
    was_pressed = False
    print("You: ", end="", flush=True)
    
    # Dual Input Loop
    while True:
        # --- 1. Terminal Input (Non-blocking so the button can be checked) ---
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.readline().strip()

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nShutting down the system. Goodbye!")
                break

            if user_input:
                messages.append({"role": "user", "content": user_input})
                messages = handle_slm_interaction(messages)

            print("You: ", end="", flush=True)

        # --- 2. Button Input (Periodic Check) ---
        if button.is_pressed and not was_pressed:
            # Rising edge (button has just been pressed)
             
            button_prompt = PROMPT_TEMPLATE
            
            print("\n[DETECTED: BUTTON PRESSED] -> Starting automatic control mode via SLM.")
            
            messages.append({"role": "user", "content": button_prompt})
            messages = handle_slm_interaction(messages)

            print("You: ", end="", flush=True)
            
            was_pressed = True

        elif not button.is_pressed and was_pressed:
            was_pressed = False
            
        time.sleep(BUTTON_CHECK_INTERVAL)

if __name__ == "__main__":
    interactive_mode(MODEL)
