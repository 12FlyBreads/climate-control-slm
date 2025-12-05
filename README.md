# ☁️ Intelligent Climate Control - Edge GenAI 

**Intelligent Climate Control** is an edge-AI system running entirely on the **Raspberry Pi 5**, capable of monitoring environmental conditions (temperature, humidity, and pressure) in real time and making autonomous climate-regulation decisions using a **Small Language Model (SLM)** executed locally — with no cloud dependency.

The project combines **hardware sensing**, **simulated actuators (LEDs)**, and **on-device** generative AI through structured function calling, enabling natural-language interaction and intelligent environmental control.

---

## 🚀 Key Features

- 🌡️ **Real-time environmental monitoring** (temperature, humidity, pressure)  
- 🤖 **Fully on-device SLM inference** — no internet or cloud required  
- 🔧 **Simulated actuators** (cooling, heating, and status LEDs) 
- ⚡ **Optimized for Raspberry Pi 5 performance**
- 🧠 **Function Calling** for structured communication between AI and hardware
- 👆 **Physical push button** for quick manual actions 

---

## 🧠 How It Works

Sensor Data → Preprocessing → SLM Analysis → Climate Decision → Actuator Response

1.Reads live environmental data using DHT22 and BMP280 sensors
2.Processes values and forwards them to the SLM
3.The on-device SLM analyzes the context and determines the best climate action
4.The system activates the appropriate actuator (LEDs: cooling/heating/status)
5.Optional: user interacts via natural language prompts 

---

## 🏗️ Project Structure

```bash
.
├── src/
│   ├── config.yaml           # Configuration files
│   ├── hardware.py           # Hardware functions
│   ├── inference.py          # SLM functions
│   ├── utils.py              # Utility functions
│   └── main.py               # Main application entry point
├── install.sh                # Setup and environment automation
├── requirements.txt          # Requirements
└── README.md

```

---

## 🧰 Requirements

Python 3.9+

- Raspberry Pi 5 (with active cooling recommended)
- DHT22 (temperature + humidity sensor)
- BMP280 (barometric pressure sensor)
- 3 LEDs (cooling/heating/status)
- Push button (manual override / quick action)
- Ollama installed on the Raspberry Pi

---

## 🧩 Installation

### 1. Clone the repository
```bash
git clone https://github.com/12FlyBreads/climate-control-slm.git
cd climate-control-genai
```
### 2. Run the bash script
```bash
chmod +x install.sh
./install.sh
```
Obs.: if you are getting errors during installation, try to install each library separately.
### 3. Run the application
```bash
cd src
python3 main.py
```

---

## 👥 Authors

- **Alex Alvarez Duque**
  [GitHub](https://github.com/Alexduque14)
- **Artur Simão**
  [GitHub](https://github.com/12FlyBreads)
- **Pedro Lucas Pereira Ferreira**
  [GitHub](https://github.com/pedrolucas-pf)

Credits to Prof. Marcelo Rovai
  [GitHub](https://github.com/Mjrovai)

---
