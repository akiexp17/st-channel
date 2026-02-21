import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

interface SimCardProps {
    id: string;
    title: string;
    subject: string;
    color: string;
}

export default function SimCard({ id, title, subject, color }: SimCardProps) {
    return (
        <Link to={`/simulations/${id}`}>
            <motion.div
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.95 }}
                className="glass-card rounded-2xl overflow-hidden cursor-pointer h-[240px] flex flex-col relative group"
            >
                <div className={`absolute inset-0 opacity-20 group-hover:opacity-40 transition-opacity duration-300 ${color}`} />
                <div className="p-6 flex-grow flex flex-col justify-end z-10">
                    <span className="text-xs font-semibold uppercase tracking-wider mb-2 opacity-80">{subject}</span>
                    <h3 className="text-xl font-bold leading-tight drop-shadow-md">{title}</h3>
                </div>
            </motion.div>
        </Link>
    );
}
