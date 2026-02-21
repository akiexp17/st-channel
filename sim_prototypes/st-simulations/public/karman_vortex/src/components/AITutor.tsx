import React, { useEffect, useState } from 'react';
import { Bot, Sparkles } from 'lucide-react';

interface AITutorProps {
    windSpeed: number;
    radius: number;
}

export const AITutor: React.FC<AITutorProps> = ({ windSpeed, radius }) => {
    const [message, setMessage] = useState("こんにちは。電柱に当たる風のシミュレーションへようこそ。右のパネルで風速を上げてみて。");

    // Socratic rules simulation
    useEffect(() => {
        if (windSpeed > 8) {
            setMessage("風を限界まで強くしたね！電柱の後ろの空気が、乱暴に乱れている（乱流）のがわかる？この状態だと綺麗な渦はできないみたいだ。少し風を弱めてみる？");
        } else if (windSpeed > 1 && windSpeed < 6 && radius > 0.03 && radius < 0.1) {
            setMessage("お見事！綺麗な交互の渦、『カルマン渦列』が生まれたね！台風の日に電柱が「ヒューッ」と鳴る原因なんだよ。");
        } else if (radius > 0.2) {
            setMessage("電柱をすごく太くしたね。渦ができるタイミング（周期）がゆっくりになったのを感じる？");
        } else {
            setMessage("パラメータを変えて、綺麗な「交互の渦」が発生するバランス（レイノルズ数）を探してみて。");
        }
    }, [windSpeed, radius]);

    return (
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 w-[600px] max-w-[90vw] bg-black/60 backdrop-blur-2xl border border-white/20 rounded-2xl p-6 text-white shadow-[0_10px_50px_rgba(0,0,0,0.5)]">
            <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-cyan-400 to-purple-500 p-0.5 flex-shrink-0 relative">
                    <div className="w-full h-full bg-black rounded-full flex items-center justify-center">
                        <Bot size={24} className="text-cyan-200" />
                    </div>
                    <Sparkles size={14} className="absolute -top-1 -right-1 text-yellow-300 animate-pulse" />
                </div>
                <div className="flex-1">
                    <div className="text-xs text-cyan-400 font-bold tracking-widest mb-1">AI SOCRATIC TUTOR</div>
                    <p className="text-gray-100 leading-relaxed text-[15px]">
                        {message}
                    </p>
                </div>
            </div>
        </div>
    );
};
