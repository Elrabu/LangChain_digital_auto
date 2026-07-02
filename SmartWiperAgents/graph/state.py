from typing import TypedDict, Literal, Optional
 
class WiperState(TypedDict): #set up the complete schema for the shared state, that is used in the Graph workflow

    #define input state variables for nodes
    hood_is_open: bool
    current_wiper_mode: str
    vehicle_speed: float

    #define output state variables for node 
    safety_assessment: Optional[str]
    safety_risk_level: Optional[Literal["LOW", "MEDIUM", "HIGH"]]
    decided_action: Optional[Literal["STOP_WIPER", "KEEP_WIPER", "REDUCE_WIPER"]]
    reasoning_log: list[str]
    
    next_agent: Optional[str] # the name of the next node to be accessed, as set by the supervisor
