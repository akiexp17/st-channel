import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, Atom, Calculator, Zap, Globe2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import SimCard from '../components/ui/SimCard';

const featuredSims = [
    { id: 'karman-vortex', title: 'Karman Vortex Street', subject: 'Physics', color: 'bg-blue-500' },
    { id: 'energy-skate-park', title: 'Energy Skate Park', subject: 'Physics', color: 'bg-emerald-500' },
    { id: 'build-an-atom', title: 'Build an Atom', subject: 'Chemistry', color: 'bg-purple-500' },
    { id: 'fraction-matcher', title: 'Fraction Matcher', subject: 'Math', color: 'bg-pink-500' },
];

const subjects = [
    { name: 'Physics', icon: <Atom className="w-8 h-8" />, color: 'text-blue-400', path: '/simulations?subject=physics' },
    { name: 'Chemistry', icon: <Sparkles className="w-8 h-8" />, color: 'text-purple-400', path: '/simulations?subject=chemistry' },
    { name: 'Math', icon: <Calculator className="w-8 h-8" />, color: 'text-pink-400', path: '/simulations?subject=math' },
    { name: 'Earth Science', icon: <Globe2 className="w-8 h-8" />, color: 'text-emerald-400', path: '/simulations?subject=earth' },
    { name: 'Biology', icon: <Zap className="w-8 h-8" />, color: 'text-yellow-400', path: '/simulations?subject=biology' },
];

export default function Home() {
    return (
        <div className="pb-24">
            {/* Hero Section */}
            <section className="relative overflow-hidden pt-20 pb-32">
                <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/40 via-slate-900 to-slate-900 -z-10" />

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <h1 className="text-4xl md:text-7xl font-extrabold tracking-tight mb-8">
                            Interactive <span className="text-gradient drop-shadow-lg">Simulations</span><br /> for Science and Math
                        </h1>
                        <p className="text-xl md:text-2xl text-slate-300 max-w-3xl mx-auto mb-10 leading-relaxed font-light">
                            Engage through an intuitive, game-like environment where learning happens through exploration and discovery.
                        </p>
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                            <Link to="/simulations" className="group flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-full text-lg font-semibold transition-all hover:shadow-[0_0_30px_rgba(59,130,246,0.6)] w-full sm:w-auto">
                                Explore All Sims
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <Link to="/about" className="glass px-8 py-4 rounded-full text-lg font-semibold hover:bg-white/10 transition-colors w-full sm:w-auto">
                                For Teachers
                            </Link>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Subjects Section */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <div className="text-center mb-12">
                    <h2 className="text-3xl font-bold mb-4 drop-shadow">Browse by Subject</h2>
                </div>
                <div className="flex flex-wrap justify-center gap-6">
                    {subjects.map((sub, i) => (
                        <Link key={i} to={sub.path}>
                            <motion.div
                                whileHover={{ scale: 1.05 }}
                                className="glass rounded-2xl p-6 flex flex-col items-center justify-center gap-4 w-40 h-40 hover:bg-white/10 transition-colors shadow-lg"
                            >
                                <div className={sub.color}>{sub.icon}</div>
                                <span className="font-semibold text-sm tracking-wide">{sub.name}</span>
                            </motion.div>
                        </Link>
                    ))}
                </div>
            </section>

            {/* Featured Simulations */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <div className="flex items-center justify-between mb-8">
                    <h2 className="text-3xl font-bold drop-shadow">Featured Simulations</h2>
                    <Link to="/simulations" className="text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1">
                        View all <ArrowRight className="w-4 h-4" />
                    </Link>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {featuredSims.map((sim, i) => (
                        <motion.div
                            key={sim.id}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: i * 0.1 }}
                        >
                            <SimCard {...sim} />
                        </motion.div>
                    ))}
                </div>
            </section>
        </div>
    );
}
