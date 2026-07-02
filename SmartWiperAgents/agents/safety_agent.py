from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import json, re
from graph.state import WiperState
from langchain_core.callbacks import BaseCallbackHandler

class LLMTap(BaseCallbackHandler): #Helper Method to log LLM Inputs and Outputs
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print("═══ LLM CALL ═══")
        for msg_list in messages:
            for m in msg_list: #iterate over the messages
                print(f"[{m.type.upper()}] {m.content}") #print the message type and content
        print("════════════════")

    def on_llm_end(self, response, **kwargs):
        for gen in response.generations: #iterate over all generated responses
            for g in gen: #iterate over all response lines
                print(f"[LLM REPLY] {g.text}")
        print("════════════════\n")

llm = ChatOllama( #configure the local Ollama model
    model="llama3.1:8b",
    #callbacks=[LLMTap()],
    temperature=0.0, #temperatur of zero means allow no variantions in answers
    base_url="http://localhost:11434" #local OLLAMA endpointS
)

#full safety prompt, request the answer to be in JSON format
SAFETY_PROMPT = """You are a vehicle Safety Agent. Assess risk based on VSS signals  
and assess whether a safety risk exists IN THIS SPECIFIC SITUATION.

Important: Base your assessment STRICTLY on the values provided in the user message.
Do NOT assume any condition that is not explicitly stated.

Given the state, return a JSON object:
{
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "assessment": "<one-sentence reasoning>",
  "recommended_action": "STOP_WIPER" | "KEEP_WIPER" | "REDUCE_WIPER"
}

Return ONLY valid JSON, nothing else.
"""
 
def safety_node(state: WiperState) -> WiperState: #graph node function, that accepts current state and return updated state
    user = ( #get the current vehicle state
        f"hood_is_open={state['hood_is_open']}, "
        f"current_wiper_mode={state['current_wiper_mode']}, "
        f"vehicle_speed={state['vehicle_speed']} km/h"
    )
    response = llm.invoke([ #invoke the LLm call
        SystemMessage(content=SAFETY_PROMPT), #hand the Safety prompt over to the LLM as a Behavior guideline
        HumanMessage(content=user) #transfer the user data containing the current vehicle state
    ]).content
 
    match = re.search(r'\{.*\}', response, re.DOTALL) #extract thefirst JSON object from the response using Regex
    data = json.loads(match.group(0)) #save found JSON Strings into a dictionary
    
    #save the state values from the LLM response into the current state
    state["safety_risk_level"]  = data["risk_level"] 
    state["safety_assessment"]  = data["assessment"]
    state["decided_action"]     = data["recommended_action"]
    state.setdefault("reasoning_log", []).append( #create empty LOG list 
        f"[Safety] {data['risk_level']}: {data['assessment']}" #add the safety assesment
    )
    return state #return the updated state to the Graph
