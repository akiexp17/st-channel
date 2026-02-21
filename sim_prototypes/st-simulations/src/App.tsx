import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Home from './pages/Home';
import Simulations from './pages/Simulations';
import Player from './pages/Player';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-900 text-slate-50 font-sans selection:bg-blue-500/30">
        <Navbar />
        <main className="pt-16 min-h-[calc(100vh-4rem)]">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/simulations" element={<Simulations />} />
            <Route path="/simulations/:id" element={<Player />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
