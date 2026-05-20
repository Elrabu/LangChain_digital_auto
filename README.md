# LangGraph_DigitalAuto
Setup Guide to set up a LangGraph-based multi-agent system that uses a locally running Ollama LLM to interpret vehicle sensor data like rain intensity or hood status from the Kuksa data broker and autonomously sets the appropriate windshield wiper mode via VSS actuators.

## Hierarchy
```
 ├── SmartWiperAgents
 ├── SmartWiperApp
```

## Velocitas Runtime Setup
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







