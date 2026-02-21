import { useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import { WebGLFluid } from '../fluid/WebGLFluid';

export interface FluidCanvasHandle {
    setWindSpeed: (val: number) => void;
    setObstacleRadius: (val: number) => void;
    setViscosity: (val: number) => void;
}

export const FluidCanvas = forwardRef<FluidCanvasHandle>((_, ref) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const fluidRef = useRef<WebGLFluid | null>(null);

    useEffect(() => {
        if (!canvasRef.current) return;

        // Initialize standard fullscreen fluid
        const fluid = new WebGLFluid(canvasRef.current);
        fluidRef.current = fluid;

        const handleResize = () => {
            fluid.resize(window.innerWidth, window.innerHeight);
        };
        handleResize();
        window.addEventListener('resize', handleResize);

        // Initial parameters for Karman Vortex
        fluid.windSpeed = 2.0;
        fluid.obstacleRadius = 0.05;
        fluid.obstacleCenter = { x: 0.3, y: 0.5 }; // Position pole nicely on the left-ish side

        fluid.start();

        // Interaction splat
        let isDown = false;
        const handleDown = (e: MouseEvent | TouchEvent) => { isDown = true; triggerSplat(e); };
        const handleUp = () => { isDown = false; };
        const handleMove = (e: MouseEvent | TouchEvent) => { if (isDown) triggerSplat(e); };

        const triggerSplat = (e: MouseEvent | TouchEvent) => {
            const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
            const clientY = 'touches' in e ? e.touches[0].clientY : e.clientY;

            const x = clientX / window.innerWidth;
            const y = clientY / window.innerHeight;

            // Target the ball
            const obX = fluid.obstacleCenter.x;
            const obY = fluid.obstacleCenter.y;
            const dirX = obX - x;
            const dirY = obY - y;
            const len = Math.sqrt(dirX * dirX + dirY * dirY);

            // Give a strong directional burst
            const intensity = 30.0;
            const dx = len > 0.001 ? (dirX / len) * intensity : 0;
            const dy = len > 0.001 ? (dirY / len) * intensity : 0;

            const time = Date.now() * 0.005;
            fluid.splat(x, y, dx, dy, {
                r: Math.sin(time) * 0.5 + 0.5,
                g: 0.8,
                b: Math.cos(time) * 0.5 + 1.0
            });
        };

        const canvas = canvasRef.current;
        canvas.addEventListener('mousedown', handleDown);
        window.addEventListener('mouseup', handleUp);
        window.addEventListener('mousemove', handleMove);
        canvas.addEventListener('touchstart', handleDown);
        window.addEventListener('touchend', handleUp);
        window.addEventListener('touchmove', handleMove);

        return () => {
            window.removeEventListener('resize', handleResize);
            canvas.removeEventListener('mousedown', handleDown);
            window.removeEventListener('mouseup', handleUp);
            window.removeEventListener('mousemove', handleMove);
            canvas.removeEventListener('touchstart', handleDown);
            window.removeEventListener('touchend', handleUp);
            window.removeEventListener('touchmove', handleMove);
            fluid.stop();
        };
    }, []);

    useImperativeHandle(ref, () => ({
        setWindSpeed: (val: number) => {
            if (fluidRef.current) fluidRef.current.windSpeed = val;
        },
        setObstacleRadius: (val: number) => {
            if (fluidRef.current) fluidRef.current.obstacleRadius = val;
        },
        setViscosity: (val: number) => {
            // Scale viscosity to appropriate shader internal range
            if (fluidRef.current) fluidRef.current.viscosity = val;
        }
    }));

    return (
        <canvas
            ref={canvasRef}
            className="absolute top-0 left-0 w-full h-full cursor-crosshair touch-none"
        />
    );
});

FluidCanvas.displayName = 'FluidCanvas';
