import { useRef, useState, useEffect } from 'react';
import { FluidCanvas, FluidCanvasHandle } from './components/FluidCanvas';
import { Controls } from './components/Controls';
import { AITutor } from './components/AITutor';

function App() {
    const fluidRef = useRef<FluidCanvasHandle>(null);

    const [windSpeed, setWindSpeed] = useState(2.0);
    const [radius, setRadius] = useState(0.05);
    const [viscosity, setViscosity] = useState(0.5);

    useEffect(() => {
        if (fluidRef.current) {
            fluidRef.current.setWindSpeed(windSpeed);
        }
    }, [windSpeed]);

    useEffect(() => {
        if (fluidRef.current) {
            fluidRef.current.setObstacleRadius(radius);
        }
    }, [radius]);

    useEffect(() => {
        if (fluidRef.current) {
            fluidRef.current.setViscosity(viscosity);
        }
    }, [viscosity]);

    return (
        <div className="relative w-full h-screen overflow-hidden bg-black font-sans">
            {/* Background WebGL Canvas */}
            <FluidCanvas ref={fluidRef} />

            {/* Overlay UI */}
            <div className="pointer-events-none absolute inset-0 text-white p-6 z-10">
                <h1 className="text-3xl font-extrabold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500 mb-2">
                    NEXTGEN SIMLAB
                </h1>
                <p className="text-sm text-gray-400 font-mono tracking-wide">EXPERIMENT: KARMAN VORTEX STREET</p>
            </div>

            {/* Interactive UI Panels (pointer-events-auto re-enables interaction) */}
            <div className="absolute inset-0 pointer-events-none z-20">
                <div className="pointer-events-auto h-full relative">
                    <Controls
                        windSpeed={windSpeed} setWindSpeed={setWindSpeed}
                        radius={radius} setRadius={setRadius}
                        viscosity={viscosity} setViscosity={setViscosity}
                    />
                    <AITutor windSpeed={windSpeed} radius={radius} />
                </div>
            </div>
        </div>
    );
}

export default App;
