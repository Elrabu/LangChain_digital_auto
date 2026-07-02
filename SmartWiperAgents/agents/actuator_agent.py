from graph.state import WiperState

_vehicle_ref = None # global reference to velocitas vehicle object
 
def set_vehicle(v): #setter function to enable an injection of the vehilce object from outside the file
    global _vehicle_ref #access global variable
    _vehicle_ref = v #save variable v into global variable
 
async def actuator_node(state: WiperState) -> WiperState: #asynchronous Graph node, since Velocitas app works async
    action = state.get("decided_action")

    #based on the final verdict, set the responsive wiper mode
    if action == "STOP_WIPER":
        await _vehicle_ref.Body.Windshield.Front.Wiping.Mode.set("OFF")
        msg = "Executed: Wiper.Mode = OFF via Velocitas SDK"
    elif action == "REDUCE_WIPER":
        await _vehicle_ref.Body.Windshield.Front.Wiping.Mode.set("SLOW")
        msg = "Executed: Wiper.Mode = SLOW"
    else:
        msg = "Executed: no change (KEEP_WIPER)"
 
    state.setdefault("reasoning_log", []).append(f"[Actuator] {msg}") #append reasoning log to "reasoning_log" list
    return state #return updated state
