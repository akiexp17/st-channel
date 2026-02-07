
import fluids
import numpy as np

def calculate_system_curve():
    """
    Calculates the system curve (Head vs Flow Rate) for a water transfer system.
    
    System Description:
    - Transferring water from a ground storage tank to an elevated tank.
    - Elevation Difference: 15 meters
    - Pipe: DN 50 (2-inch), Schedule 40 Steel Pipe
    - Length: 100 meters
    - Fittings: 4x 90-degree Elbows, 1x Globe Valve, 1x Entrance, 1x Exit
    """
    
    # 1. Define Fluid Properties (Water at 25 degC)
    # Using simple properties for clarity, though fluids has rigorous property databases
    rho = 997.04 # kg/m^3
    mu = 0.00089 # Pa*s
    
    # 2. Define Piping Geometry
    # Get standard pipe dimensions (Schedule 40 Steel)
    # NPS 2 (DN 50)
    pipe = fluids.piping.nearest_pipe(NPS=2, schedule='40')
    D = pipe[1] # Inner diameter in meters (approx 0.0525 m)
    roughness = 4.5e-5 # m for commercial steel (explicit)
    
    L = 100.0 # meters
    elevation_rise = 15.0 # meters
    
    # 3. Define Fittings (Loss Coefficients / K-factors)
    # Using Crane 410 or similar standard methods provided by fluids
    # K factors often depend on diameter or friction factor, but fluids handles this.
    
    # We will sum up the minor loss coefficients (K) later or calculate dynamic losses
    
    print(f"--- System Design Parameters ---")
    print(f"Fluid: Water @ 25C (rho={rho} kg/m3, mu={mu} Pa*s)")
    print(f"Pipe: NPS 2 Sch 40 (ID = {D*1000:.2f} mm)")
    print(f"Roughness: {roughness*1000:.3f} mm")
    print(f"Length: {L} m, Elevation: {elevation_rise} m")
    print("-" * 30)
    print(f"{'Flow (L/min)':<15} | {'Velocity (m/s)':<15} | {'Re':<10} | {'Friction (f)':<12} | {'S Head (m)':<10} | {'D Head (m)':<10} | {'Total Head (m)':<15}")
    print("-" * 100)

    # Calculate for a range of flow rates
    flow_rates_lpm = [50, 100, 150, 200, 250, 300]
    
    results = []

    for Q_lpm in flow_rates_lpm:
        # Convert Flow Rate to SI (m^3/s)
        Q = Q_lpm * (1/60000) # L/min -> m3/s
        
        # Velocity
        area = np.pi * D**2 / 4
        V = Q / area
        
        # Reynolds Number
        Re = fluids.core.Reynolds(V, D, rho, mu)
        
        # Friction Factor (Darcy-Weisbach)
        # Colebrook is standard for turbulent flow
        fd = fluids.friction.friction_factor(Re, eD=roughness/D)
        
        # Major Loss (Pipe Friction) -> Darcy-Weisbach Equation
        # Head Loss = f * (L/D) * (V^2 / 2g)
        g = 9.80665
        h_major = fd * (L/D) * (V**2 / (2*g))
        
        # Minor Losses (Fittings)
        K_total = 0
        
        # Entrance (Sharp-edged)
        K_total += 0.5 # Standard K for sharp entrance
        
        # Exit (Pipe to large tank)
        K_total += 1.0 # Standard K for exit
        
        # Elbows (4x Standard 90 deg, threaded)
        # Using simple Crane method equivalent: K ~ 30*fT (turbulent friction factor)
        # Or use fluids specific functions
        # For simplicity in this demo, accessing specific fitting K from fluids library
        # Elbow calculation moved to manual method below
        # Actually Crane 410 standard threaded elbow is simpler to look up often, but let's use a generic bend here
        # or specific function:
        # fluids.fittings.K_Crane_410_pipe_fittings(D, type='elbow_90_standard_threaded')
        # Note: methods vary, sticking to a robust one:
        
        # Let's use the '3K' method or '2K' method if available, or just a constant for demo clarity if needed.
        # But fluids has `fluids.fittings.ELBOW_90_LONG_RADIUS_THREADED` etc.
        # Let's use K values for standard fittings
        K_elbow = 0.75 # Generic standard elbow estimate if function call gets complex
        # Let's try to allow fluids to calculate it if possible. 
        # Using Crane K = 30 * fT
        fT = fluids.friction.friction_factor(fluids.core.Reynolds(1e6, D, rho, mu), roughness/D) # Fully turbulent friction
        K_elbow_crane = 30 * fT
        K_total += 4 * K_elbow_crane
        
        # Globe Valve (Fully Open)
        # Crane K = 340 * fT
        K_valve = 340 * fT
        K_total += 1 * K_valve
        
        # Minor Head Loss
        h_minor = K_total * (V**2 / (2*g))
        
        # Total Dynamic Head Loss
        h_dynamic = h_major + h_minor
        
        # Static Head (Elevation)
        h_static = elevation_rise
        
        # Total Pump Head Required
        h_total = h_static + h_dynamic
        
        print(f"{Q_lpm:<15.1f} | {V:<15.2f} | {Re:<10.0f} | {fd:<12.4f} | {h_static:<10.1f} | {h_dynamic:<10.2f} | {h_total:<15.2f}")
        
        results.append((Q_lpm, h_total))

    # Design Point calculation (e.g. at 200 L/min)
    Q_design_lpm = 200
    Q_design = Q_design_lpm / 60000
    V_design = Q_design / (np.pi * D**2 / 4)
    P_hydraulic_watts = Q_design * float(results[3][1]) * 9.81 * rho # Approx
    
    print("-" * 100)
    print(f"Design Point ({Q_design_lpm} L/min): Required Pump Head = {results[3][1]:.2f} m")
    print(f"Hydraulic Power = {P_hydraulic_watts:.2f} W")

if __name__ == "__main__":
    calculate_system_curve()
