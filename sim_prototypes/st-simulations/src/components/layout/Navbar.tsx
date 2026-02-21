import { Link } from 'react-router-dom';
import { Beaker, Menu, Search, X } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <nav className="fixed top-0 inset-x-0 z-50 glass border-b border-white/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center gap-2">
                        <Link to="/" className="flex items-center gap-2 group">
                            <div className="p-2 bg-blue-500/20 rounded-lg group-hover:bg-blue-500/30 transition-colors">
                                <Beaker className="w-6 h-6 text-blue-400" />
                            </div>
                            <span className="font-bold text-xl tracking-tight">ST Simulations</span>
                        </Link>
                    </div>

                    <div className="hidden md:block">
                        <div className="ml-10 flex items-baseline space-x-8">
                            <Link to="/simulations" className="hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium transition-colors">All Sims</Link>
                            <Link to="/simulations?subject=physics" className="hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium transition-colors">Physics</Link>
                            <Link to="/simulations?subject=math" className="hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium transition-colors">Math</Link>
                            <Link to="/simulations?subject=chemistry" className="hover:text-blue-400 px-3 py-2 rounded-md text-sm font-medium transition-colors">Chemistry</Link>
                        </div>
                    </div>

                    <div className="hidden md:flex items-center gap-4">
                        <button className="text-slate-300 hover:text-white transition-colors p-2 rounded-full hover:bg-white/5">
                            <Search className="w-5 h-5" />
                        </button>
                        <a href="#" className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all hover:shadow-[0_0_15px_rgba(59,130,246,0.5)]">
                            Sign In
                        </a>
                    </div>

                    <div className="-mr-2 flex md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="inline-flex items-center justify-center p-2 rounded-md text-slate-400 hover:text-white hover:bg-white/5 focus:outline-none"
                        >
                            <span className="sr-only">Open main menu</span>
                            {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        transition={{ duration: 0.2 }}
                        className="md:hidden glass border-t border-white/5"
                    >
                        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                            <Link to="/simulations" onClick={() => setIsOpen(false)} className="hover:bg-white/5 block px-3 py-2 rounded-md text-base font-medium">All Sims</Link>
                            <Link to="/simulations?subject=physics" onClick={() => setIsOpen(false)} className="hover:bg-white/5 block px-3 py-2 rounded-md text-base font-medium">Physics</Link>
                            <Link to="/simulations?subject=math" onClick={() => setIsOpen(false)} className="hover:bg-white/5 block px-3 py-2 rounded-md text-base font-medium">Math</Link>
                            <a href="#" className="mt-4 block text-center bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-base font-medium">Sign In</a>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
}
