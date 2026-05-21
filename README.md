# LangGraph_DigitalAuto
Setup Guide to set up a LangGraph-based multi-agent system that uses a locally running Ollama LLM to interpret vehicle sensor data like rain intensity or hood status from the Kuksa data broker and autonomously sets the appropriate windshield wiper mode via VSS actuators.

## Hierarchy
```
 ├── SmartWiperAgents
 ├── SmartWiperApp
```

## Velocitas Runtime Setup (SmartWiperApp)
this creates the Velocitas-Runtime (Kuksa Databroker, MQTT, Mock-Service) that is used by the "vehicle" model inside "SmartWiperAgents"

### 1. Clone the template repo
```
git clone https://github.com/eclipse-velocitas/vehicle-app-python-template.git SmartWiperApp
cd SmartWiperApp
```

### 2. pull the packages declared in .velocitas.json
```
velocitas init
```

### 3. Sync devcontainer / scripts / workflows
```
velocitas sync
```

### 4. Start Velocitas Runtime
```
velocitas exec runtime-local up
```

## SmartWiperAgents Setup

SmartWiperAgents is a multi-agent system using LangGraph that responds to events from the Velocitas Vehicle Runtime and makes and decides on the windshield wiper mode based on the input.

### 1. Requirement checks

```
python3.12 --version
```
if not installed:
```
 sudo apt install python3.12
```

### 2. Local Ollama installation

install ubuntu binary and set up a system service so it can run in the background:
```
curl -fsSL https://ollama.com/install.sh | sh
```

start it with
```
ollama serve
```

pull the Ollama 3.1:8b model

```
ollama pull llama3.1:8b
```

### 3. Setup virtual environment
```
python3.12 -m venv .venv
```
to activate the environment for the rest of the setup
```
source .venv/bin/activate
```

### 4. install requirements
```
pip install -r requirements.txt
```

### 5. add __init.py__ 
to define the directories as packages and allow import:
```
touch app/__init__.py
```
agents
graph








