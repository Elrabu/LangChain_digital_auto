# LangGraph_DigitalAuto
Setup Guide to set up a LangGraph-based multi-agent system that uses a locally running Ollama LLM to interpret vehicle sensor data like rain intensity or hood status from the Kuksa data broker and autonomously sets the appropriate windshield wiper mode via VSS actuators.

## Velocitas Runtime Setup
this creates the Velocitas-Runtime (Kuksa Databroker, MQTT, Mock-Service) that is used by the "vehicle" model inside "SmartWiperAgents"

### 1. Clone the template repo
