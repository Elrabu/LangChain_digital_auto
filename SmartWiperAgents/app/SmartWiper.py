import asyncio, signal, warnings, sys
warnings.filterwarnings("ignore", category=DeprecationWarning)

from timing import timer  
from memory_tracker import memory 

from velocitas_sdk.vehicle_app import VehicleApp
from vehicle import Vehicle, vehicle
from graph.wiper_graph import build_graph
from agents.actuator_agent import set_vehicle
from langchain_core.tracers.langchain import wait_for_all_tracers 

class SmartWiperApp(VehicleApp): #class that inherits from the VehicleApp class

    def __init__(self, vehicle_client: Vehicle): #constructor enables app.run() or subscription to the vehicle app
        super().__init__() #call the base class constructor (VehicleApp)
        self.Vehicle = vehicle_client #save the Vehicle Client as an instance attribute (connection to VehicleApp)
        self.graph   = build_graph() #compile the LangGraph workflow
        self.program_done   = asyncio.Event() #define signal (can be set or not set)
        self.current_wiper_mode = "OFF" #set current wiper mode
        set_vehicle(vehicle_client) #call the set_vehicle function from the "actuator_agent"

    async def on_start(self): #lifecicle hook that is called by the Velocitas App on startup
        memory.start_peak_sampler() 

        async def on_hood_changed(reply): #callback function, that is triggered if the hood status changes
            
            hood_Open_Status = reply.get(self.Vehicle.Body.Hood.IsOpen) #extract the current data point from hood.IsOpen
            is_hood_open: bool = bool(hood_Open_Status.value) #change the data point into a python bool variable
            
            #get current vehicle status
            mode_reply  = await self.Vehicle.Body.Windshield.Front.Wiping.Mode.get()
            speed_reply = await self.Vehicle.Speed.get()
            current_wiper_mode  = str(mode_reply.value) if mode_reply.value else "OFF"
            vehicle_speed = float(speed_reply.value or 0.0)

            print(f"[DEBUG] hood_open={is_hood_open!r}  mode={current_wiper_mode!r}  speed={vehicle_speed!r}")

            initial_state = { #set initial state for the LangGraph execution
                "hood_is_open":       is_hood_open,
                "current_wiper_mode": current_wiper_mode,
                "vehicle_speed":      vehicle_speed,
                "safety_assessment":  None,
                "safety_risk_level":  None,
                "decided_action":     None,
                "reasoning_log":      [],
                "next_agent":         None,
            }

            print("[Velocitas -> Agents] Invoking LangGraph...")
            final = await self.graph.ainvoke(initial_state) #start the LangGrah workflow asynchronous and wait for final result

            timer.mark_verdict_received()

            #print the content of the reasoning log:
            print("\n=== AGENT REASONING TRACE ===")
            for line in final["reasoning_log"]:
                print(" ", line)
            print(f"  Final action: {final['decided_action']}")
            print("=============================\n")

            self.program_done.set() #set the done flag here as as set
        
        await self.Vehicle.Body.Hood.IsOpen.subscribe(on_hood_changed) #register the VSS vehicle signal where on_hood_changed is called on changes to the signal
        print("[Velocitas] Listener registriert")

        timer.mark_startup_complete()

        await self.program_done.wait()                # block asynchonous until the done flag is set
        print("[Velocitas] App Closed.")

        wait_for_all_tracers() # check that all the tracing data is correctly sent

        timer.print_summary()
        memory.print_summary()  

        sys.exit(0)                            # exit the progam clean, stopping all running threads

async def main(): #
    app = SmartWiperApp(vehicle) #create Instance of the SmartWiper App and the "vehicle" Instance
    await app.run()

#get the current event loop 
LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop) #add a stop signal that can be triggered
LOOP.run_until_complete(main()) #start the event loop so that it runs until the program finished executing
