import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Maximize2, Share2, Info, BookOpen } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Player() {
    const { id } = useParams();

    // Mocking data based on standard ID
    const isKarman = id === 'karman-vortex';
    const title = isKarman ? 'Karman Vortex Street' : (id || 'Simulation').replace(/-/g, ' ');

    return (
        <div className="max-w-[1600px] mx-auto p-4 sm:p-6 lg:p-8 h-full flex flex-col lg:flex-row gap-6">
            {/* Main Player Area */}
            <div className="flex-1 flex flex-col">
                <div className="flex items-center justify-between mb-4">
                    <Link to="/simulations" className="text-slate-400 hover:text-white flex items-center gap-2 transition-colors font-medium">
                        <ArrowLeft className="w-5 h-5" /> Back to Sims
                    </Link>
                    <div className="flex gap-2">
                        <button className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors border border-white/5 hover:border-white/10 group" title="Share">
                            <Share2 className="w-5 h-5 text-slate-300 group-hover:text-white transition-colors" />
                        </button>
                        <button className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors border border-white/5 hover:border-white/10 group" title="Fullscreen">
                            <Maximize2 className="w-5 h-5 text-slate-300 group-hover:text-white transition-colors" />
                        </button>
                    </div>
                </div>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="w-full aspect-[4/3] lg:aspect-video bg-slate-950 rounded-2xl overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)] border border-white/10 flex items-center justify-center relative group"
                >
                    {isKarman ? (
                        <iframe
                            src="/karman_vortex/index.html"
                            className="w-full h-full border-0 absolute inset-0 bg-white"
                            title={title}
                        />
                    ) : (
                        <div className="text-center p-8">
                            <div className="w-20 h-20 mx-auto mb-6 relative">
                                <div className="absolute inset-0 border-4 border-t-blue-500 border-r-blue-500 border-b-transparent border-l-transparent rounded-full animate-spin"></div>
                                <div className="absolute inset-2 border-4 border-t-purple-500 border-l-purple-500 border-b-transparent border-r-transparent rounded-full animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1.5s' }}></div>
                            </div>
                            <h2 className="text-2xl font-bold mb-2 capitalize drop-shadow">Loading {title}...</h2>
                            <p className="text-slate-400">Interactive simulation environment loading.</p>
                        </div>
                    )}
                </motion.div>
            </div>

            {/* Side Panel Metadata */}
            <motion.aside
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="w-full lg:w-80 xl:w-96 flex-shrink-0 flex flex-col gap-4 mt-6 lg:mt-[3.5rem]"
            >
                <div className="glass p-6 rounded-2xl shadow-xl border border-white/5">
                    <h1 className="text-2xl font-bold mb-3 capitalize drop-shadow">{title}</h1>
                    <div className="flex flex-wrap gap-2 mb-6">
                        <span className="px-2.5 py-1 text-xs font-semibold bg-blue-500 bg-opacity-20 text-blue-300 rounded border border-blue-500/20">Physics</span>
                        {isKarman && <span className="px-2.5 py-1 text-xs font-semibold bg-emerald-500 bg-opacity-20 text-emerald-300 rounded border border-emerald-500/20">Fluid Dynamics</span>}
                        <span className="px-2.5 py-1 text-xs font-semibold bg-white/5 text-slate-300 rounded border border-white/10">v1.2.0</span>
                    </div>

                    <div className="space-y-6">
                        <div>
                            <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2 mb-3">
                                <Info className="w-4 h-4" /> About
                            </h3>
                            <p className="text-slate-300 text-sm leading-relaxed">
                                {isKarman
                                    ? "Explore the fascinating phenomenon of the Kármán vortex street—a repeating pattern of swirling vortices caused by a process known as vortex shedding. Adjust fluid viscosity and flow speed to see how it affects the wake."
                                    : "Explore the depths of scientific and mathematical concepts through interactive play. Adjust variables, test hypotheses, and discover the underlying rules that govern our universe."}
                            </p>
                        </div>

                        <div className="pt-6 border-t border-white/5">
                            <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2 mb-4">
                                <BookOpen className="w-4 h-4" /> For Teachers
                            </h3>
                            <div className="space-y-3">
                                <button className="w-full py-2.5 px-4 rounded-xl border border-white/10 hover:border-blue-500/50 hover:bg-blue-500/10 transition-all text-sm font-medium flex items-center justify-center gap-2">
                                    Learning Goals
                                </button>
                                <button className="w-full py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white transition-all hover:shadow-[0_0_15px_rgba(59,130,246,0.4)] text-sm font-medium border border-transparent">
                                    Download Lesson Plan
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </motion.aside>
        </div>
    );
}
