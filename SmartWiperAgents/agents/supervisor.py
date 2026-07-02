from graph.state import WiperState

def supervisor_node(state: WiperState) -> WiperState: #local routing node, rule based
    # Input defaults (sensor values)
    state.setdefault("hood_is_open",       False)
    state.setdefault("current_wiper_mode", "OFF")
    state.setdefault("vehicle_speed",      0.0)

    # Working memory defaults
    state.setdefault("reasoning_log",      [])
    state.setdefault("safety_assessment",  None)
    state.setdefault("safety_risk_level",  None)
    state.setdefault("decided_action",     None)

    if state.get("safety_assessment") is None: #if safety agent has not yet run, route to safety agent
        decision = "safety_agent"
    elif state.get("decided_action") is None: #if safety agent is finished, but acutator was not yet run, route to acutator agent
        decision = "actuator_agent"
    else:
        decision = "END" #end Graph execution if the state of both nodes is not none

    state["next_agent"] = decision #save routing decision in the state
    state["reasoning_log"].append(f"[Supervisor] → {decision}") #add routing decision to the reasoning log
    return state #return updated state
