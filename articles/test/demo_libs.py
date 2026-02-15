
# Python Library Demo Script
# 
# This script demonstrates the usage of three powerful Python libraries:
# 1. Pint (Unit handling)
# 2. Fluids (Fluid dynamics)
# 3. AnaStruct (Structural analysis)
#
# Note: You need to install these libraries to run this script:
# pip install pint fluids anastruct

import sys

def demo_pint():
    print("\n--- Pint Demo (Unit Handling) ---")
    try:
        from pint import UnitRegistry
        ureg = UnitRegistry()
        
        # 1. Basic Conversion
        distance = 10 * ureg.meter + 50 * ureg.centimeter
        print(f"10m + 50cm = {distance} = {distance.to(ureg.inch):.2f}")
        
        # 2. Physics Calculation (Velocity)
        time = 5 * ureg.second
        velocity = distance / time
        print(f"Velocity: {velocity} = {velocity.to(ureg.km / ureg.hour):.2f}")
        
        # 3. Dimensionality Check (Error handling)
        try:
            force = distance + time # Impossible
        except Exception as e:
            print(f"Correctly caught error for invalid addition: {e}")
            
    except ImportError:
        print("Pint is not installed. Run `pip install pint` to test.")

def demo_fluids():
    print("\n--- Fluids Demo (Fluid Dynamics) ---")
    try:
        from fluids.friction import friction_factor
        from fluids.core import Reynolds
        
        # 1. Calculate Reynolds Number
        # Water at 20C flowing in a 50mm pipe at 2 m/s
        V = 2.0 # m/s
        D = 0.05 # m
        rho = 998.2 # kg/m3 (density of water)
        mu = 1.002e-3 # Pa*s (viscosity)
        
        Re = Reynolds(V=V, D=D, rho=rho, mu=mu)
        print(f"Reynolds Number (Re): {Re:.2f}")
        
        # 2. Calculate Friction Factor (Darcy-Weisbach)
        # Assuming smooth pipe (roughness e = 0)
        fd = friction_factor(Re=Re, eD=0)
        print(f"Darcy Friction Factor: {fd:.5f}")
        
    except ImportError:
        print("Fluids is not installed. Run `pip install fluids` to test.")

def demo_anastruct():
    print("\n--- AnaStruct Demo (2D Structure) ---")
    try:
        from anastruct import SystemElements
        ss = SystemElements()
        
        # 1. Define Structure (Simple Beam)
        # Node 1 at (0,0), Node 2 at (10,0)
        ss.add_element(location=[[0, 0], [10, 0]])
        
        # 2. Add Support
        ss.add_support_hinged(node_id=1)
        ss.add_support_roll(node_id=2, direction=2)
        
        # 3. Add Load (Point load of 10kN at center)
        ss.point_load(node_id=1, Magnitude=-10) # Applying at node 1 for simplicity here, conceptually mid-span
        # Better: add q-load
        ss.q_load(element_id=1, q=-5) # Distributed load 5N/m
        
        # 4. Solve
        ss.solve()
        
        print("Structure solved. Reaction forces:")
        print(ss.get_node_results_system(node_id=1))
        
        # Note: ss.show_structure() would pop up a plot window
        print("Plots generated (if running in GUI environment).")
        
    except ImportError:
        print("AnaStruct is not installed. Run `pip install anastruct` to test.")

if __name__ == "__main__":
    demo_pint()
    demo_fluids()
    demo_anastruct()
