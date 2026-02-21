import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter } from 'lucide-react';
import SimCard from '../components/ui/SimCard';

const allSims = [
    { id: 'karman-vortex', title: 'Karman Vortex Street', subject: 'Physics', color: 'bg-blue-500' },
    { id: 'energy-skate-park', title: 'Energy Skate Park', subject: 'Physics', color: 'bg-emerald-500' },
    { id: 'build-an-atom', title: 'Build an Atom', subject: 'Chemistry', color: 'bg-purple-500' },
    { id: 'fraction-matcher', title: 'Fraction Matcher', subject: 'Math', color: 'bg-pink-500' },
    { id: 'plate-tectonics', title: 'Plate Tectonics', subject: 'Earth Science', color: 'bg-orange-500' },
    { id: 'natural-selection', title: 'Natural Selection', subject: 'Biology', color: 'bg-yellow-500' },
    { id: 'circuit-construction', title: 'Circuit Construction', subject: 'Physics', color: 'bg-blue-600' },
    { id: 'balancing-equations', title: 'Balancing Equations', subject: 'Chemistry', color: 'bg-purple-600' },
];

const subjects = ['All', 'Physics', 'Chemistry', 'Math', 'Earth Science', 'Biology'];

export default function Simulations() {
    const [activeSubject, setActiveSubject] = useState('All');
    const [searchQuery, setSearchQuery] = useState('');

    const filteredSims = allSims.filter(sim => {
        const matchesSubject = activeSubject === 'All' || sim.subject === activeSubject;
        const matchesSearch = sim.title.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesSubject && matchesSearch;
    });

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col md:flex-row gap-8">
            {/* Sidebar Filters */}
            <aside className="w-full md:w-64 flex-shrink-0">
                <div className="glass p-6 rounded-2xl sticky top-24 shadow-lg border border-white/5">
                    <h2 className="text-xl font-bold mb-6 flex items-center gap-2 drop-shadow">
                        <Filter className="w-5 h-5 text-blue-400" /> Filters
                    </h2>

                    <div className="space-y-6">
                        <div>
                            <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-3">Subjects</h3>
                            <div className="space-y-2">
                                {subjects.map(subject => (
                                    <button
                                        key={subject}
                                        onClick={() => setActiveSubject(subject)}
                                        className={`block w-full text-left px-3 py-2 rounded-lg transition-colors focus:outline-none ${activeSubject === subject
                                                ? 'bg-blue-500 bg-opacity-20 text-blue-300 font-medium border border-blue-500/20'
                                                : 'hover:bg-white/10 text-slate-300 border border-transparent'
                                            }`}
                                    >
                                        {subject}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
                    <h1 className="text-3xl font-bold drop-shadow">All Simulations</h1>

                    <div className="relative w-full sm:w-72 group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" />
                        <input
                            type="text"
                            placeholder="Search simulations..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-full py-2.5 pl-10 pr-4 focus:outline-none focus:border-blue-500/50 focus:bg-slate-800 focus:ring-1 focus:ring-blue-500/50 text-sm transition-all shadow-inner"
                        />
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredSims.map((sim, i) => (
                        <motion.div
                            key={sim.id}
                            initial={{ opacity: 0, scale: 0.95, y: 10 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            transition={{ duration: 0.3, delay: i * 0.05 }}
                        >
                            <SimCard {...sim} />
                        </motion.div>
                    ))}

                    {filteredSims.length === 0 && (
                        <div className="col-span-full py-16 text-center text-slate-400 glass rounded-2xl border border-white/5">
                            <p className="text-lg">No simulations found matching your criteria.</p>
                            <button
                                onClick={() => { setSearchQuery(''); setActiveSubject('All'); }}
                                className="mt-4 text-blue-400 hover:text-blue-300 font-medium px-4 py-2 hover:bg-white/5 rounded-lg transition-colors border border-transparent hover:border-white/10"
                            >
                                Clear all filters
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
