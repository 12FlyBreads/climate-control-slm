# === inference.py ===

# Libraries
import ollama
import json
from hardware import read_environment_data, set_led_state, get_led_status 
from typing import Dict, Any

# Global variables
AVAILABLE_TOOLS = {
    "read_environment_data": read_environment_data,
    "set_led_state": set_led_state,
    "get_led_status": get_led_status
}

SYSTEM_MESSAGE = """You are an IoT Climate Control Assistant running on a Raspberry Pi.
Your primary role is to monitor and control the environment using the provided tools.
You MUST use the tools to read sensor data or change LED states (actuators).
Always try to use the most relevant tool before providing a final answer.
Be concise and conversational in your final response."""

# --- Function Definitions ---
def get_ollama_tools() -> list:
    """
    Defines the tools available for Function Calling in Ollama.
    Returns a list of tool definitions.
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "read_environment_data",
                "description": "Reads temperature, humidity, pressure, and button state.",
                "parameters": {"type": "object", "properties": {}}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "set_led_state",
                "description": "Turns a specific LED on or off (red, yellow, green) to simulate actuator control (fan/heater).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "color": {"type": "string", "enum": ["red", "yellow", "green"], "description": "The color of the LED."},
                        "state": {"type": "string", "enum": ["on", "off"], "description": "The desired state."}
                    },
                    "required": ["color", "state"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_led_status",
                "description": "Returns the current state (on/off) of all LEDs.",
                "parameters": {"type": "object", "properties": {}}
            }
        }
    ]
    return tools

def slm_inference_with_tools(messages: list, MODEL: str) -> str:
    """
    Performs inference with Function Calling in multiple steps (multi-turn).
    Args:
        messages (list): The message history including user and system messages.
        MODEL (str): The model name to use for inference.
    Returns:
        str: The final response from the SLM after tool execution.
    """
    
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=get_ollama_tools()
    )

    if response['message'].get('tool_calls'):
        print("SLM requested Function Calling... Executing tool(s).")
        messages.append(response['message'])
        
        for tool_call in response['message']['tool_calls']:
            function_name = tool_call['function']['name']
            function_args = tool_call['function']['arguments']
            
            if function_name in AVAILABLE_TOOLS:
                function_to_call = AVAILABLE_TOOLS[function_name]
                
                function_output = function_to_call(**function_args)
                
                messages.append({
                    'role': 'tool',
                    'content': json.dumps(function_output),
                    'name': function_name
                })
                
                print(f"Result of '{function_name}' sent back to the SLM.")

            else:
                messages.append({
                    'role': 'tool',
                    'content': f"Error: Tool {function_name} not found.",
                    'name': function_name
                })

        final_response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=get_ollama_tools()
        )
        return final_response
        
    else:
        return response
        