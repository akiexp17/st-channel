import React from 'react';
import { Wind, Circle, Waves } from 'lucide-react';

interface ControlsProps {
    windSpeed: number;
    setWindSpeed: (v: number) => void;
    radius: number;
    setRadius: (v: number) => void;
    viscosity: number;
    setViscosity: (v: number) => void;
}

export const Controls: React.FC<ControlsProps> = ({
    windSpeed, setWindSpeed, radius, setRadius, viscosity, setViscosity
}) => {
    return (
        <div className="absolute right-6 top-1/2 -translate-y-1/2 w-80 bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 text-white shadow-[0_0_40px_rgba(0,0,0,0.5)] flex flex-col gap-6">
            <h2 className="text-xl font-bold tracking-wider flex items-center gap-2 mb-2">
                <span className="text-cyan-400">♦</span> Karman Vortex
            </h2>

            <div className="space-y-4">
                <div className="space-y-2">
                    <label className="flex items-center justify-between text-sm font-medium text-gray-300">
                        <span className="flex items-center gap-2"><Wind size={16} className="text-cyan-400" /> Wind Speed (Velocity)</span>
                        <span className="font-mono text-cyan-200">{windSpeed.toFixed(1)}</span>
                    </label>
                    <input
                        type="range" min="0" max="10" step="0.1"
                        value={windSpeed} onChange={e => setWindSpeed(parseFloat(e.target.value))}
                        className="w-full accent-cyan-400 cursor-pointer"
                    />
                </div>

                <div className="space-y-2">
                    <label className="flex items-center justify-between text-sm font-medium text-gray-300">
                        <span className="flex items-center gap-2"><Circle size={16} className="text-purple-400" /> Pole Diameter</span>
                        <span className="font-mono text-purple-200">{(radius * 100).toFixed(1)}</span>
                    </label>
                    <input
                        type="range" min="0.0" max="0.3" step="0.01"
                        value={radius} onChange={e => setRadius(parseFloat(e.target.value))}
                        className="w-full accent-purple-400 cursor-pointer"
                    />
                </div>

                <div className="space-y-2 pt-4 border-t border-white/10">
                    <label className="flex items-center justify-between text-sm font-medium text-gray-400">
                        <span className="flex items-center gap-2"><Waves size={16} className="text-pink-400" /> Fluid Viscosity</span>
                        <span className="font-mono text-pink-200">{viscosity.toFixed(2)}</span>
                    </label>
                    <input
                        type="range" min="0" max="1" step="0.01"
                        value={viscosity} onChange={e => setViscosity(parseFloat(e.target.value))}
                        className="w-full accent-pink-400 cursor-pointer opacity-70 hover:opacity-100 transition-opacity"
                    />
                </div>
            </div>
        </div>
    );
};
