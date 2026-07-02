from langgraph.graph import StateGraph, END
from graph.state import WiperState
from agents.supervisor import supervisor_node
from agents.safety_agent import safety_node
from agents.actuator_agent import actuator_node
 
def route(state: WiperState) -> str: #routing function for conditional edges
    return state["next_agent"] #return the current next node which is set by the supervisor
 
def build_graph(): #function to set up the LangGraph workflow
    g = StateGraph(WiperState) #create a new StateGraph with WiperState as the state schema
    
    #add all the LangGraph nodes needed for the workflow
    g.add_node("supervisor",      supervisor_node)
    g.add_node("safety_agent",    safety_node)
    g.add_node("actuator_agent",  actuator_node)
    
    g.set_entry_point("supervisor") #set the supervisor node as the entry point
    g.add_conditional_edges("supervisor", route, { #set up conditional edges based on the returned state values from the route variable
        "safety_agent":   "safety_agent",
        "actuator_agent": "actuator_agent",
        "END":            END,
    })
    
    #define concrete node order for safety and actuator agent to supervisor agent
    g.add_edge("safety_agent",   "supervisor")
    g.add_edge("actuator_agent", "supervisor")
 
    return g.compile() #compile LangGraph

graph = build_graph() # Exported for LangGraph Studio
