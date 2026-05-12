import asyncio, signal, warnings, sys
warnings.filterwarnings("ignore", category=DeprecationWarning)

from velocitas_sdk.vehicle_app import VehicleApp
from vehicle import Vehicle, vehicle
from graph.wiper_graph import build_graph
from agents.actuator_agent import set_vehicle

class SmartWiperApp(VehicleApp):

    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client
        self.graph   = build_graph()
        self._done   = asyncio.Event()
        set_vehicle(vehicle_client)

    async def on_start(self):
        await self.Vehicle.Body.Hood.IsOpen.set(False)

        async def on_hood_changed(IsOpen: bool):
            #if not IsOpen:
            #    return

            mode  = (await self.Vehicle.Body.Windshield.Front
                         .Wiping.Mode.get()).value
            speed = (await self.Vehicle.Speed.get()).value or 0.0

            initial_state = {
                "hood_is_open":       IsOpen,
                "current_wiper_mode": str(mode),
                "vehicle_speed":      float(speed),
                "safety_assessment":  None,
                "safety_risk_level":  None,
                "decided_action":     None,
                "reasoning_log":      [],
                "next_agent":         None,
            }

            print("[Velocitas → Agents] Invoking LangGraph...")
            final = await self.graph.ainvoke(initial_state)

            print("\n=== AGENT REASONING TRACE ===")
            for line in final["reasoning_log"]:
                print(" ", line)
            print(f"  Final action: {final['decided_action']}")
            print("=============================\n")

            self._done.set()

        await self.Vehicle.Body.Hood.IsOpen.subscribe(on_hood_changed)
        print("[Velocitas] Listener registriert")

        #start of the demo:
        print("[Velocitas] Scheibenwischer auf MEDIUM schalten")
        await self.Vehicle.Body.Windshield.Front.Wiping.Mode.set("MEDIUM")

        print("[Velocitas] Motorhaube öffnen")
        await self.Vehicle.Body.Hood.IsOpen.set(True)

        await self._done.wait()                # ← wartet bis Agent-Trace fertig
        print("[Velocitas] Demo abgeschlossen — App beendet.")
        sys.exit(0)                            # ← sauber, kein RuntimeError

async def main():
    app = SmartWiperApp(vehicle)
    await app.run()

LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())