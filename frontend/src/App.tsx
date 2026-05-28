/*
 * BARREL-GUARD AI — Foreign Object Detection Platform
 * Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
 */

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useWebSocket } from './hooks/useWebSocket';
import Layout from './components/layout/Layout';
import Overview from './pages/Overview';
import LiveMonitor from './pages/LiveMonitor';
import Alerts from './pages/Alerts';
import Analytics from './pages/Analytics';
import PLCStatus from './pages/PLCStatus';
import Notifications from './pages/Notifications';
import SimulationControl from './pages/SimulationControl';
import Settings from './pages/Settings';

// ✅ This is used by all pages for API calls
export const API_BASE = import.meta.env.VITE_API_URL || 'https://barrel-guard-ai-production.up.railway.app';

function AppContent() {
  useWebSocket();
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/live" element={<LiveMonitor />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/plc" element={<PLCStatus />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/simulation" element={<SimulationControl />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  );
}

export default function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}