// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Sidebar from './components/Layout/Sidebar'
import TopBar from './components/Layout/TopBar'
import Overview from './pages/Overview'
import LiveMonitor from './pages/LiveMonitor'
import Alerts from './pages/Alerts'
import Analytics from './pages/Analytics'
import PLCStatus from './pages/PLCStatus'
import Notifications from './pages/Notifications'
import Settings from './pages/Settings'
import SimulationControl from './pages/SimulationControl'
import { useWebSocket } from './hooks/useWebSocket'

export default function App() {
  useWebSocket()

  return (
    <BrowserRouter>
      <div className="flex h-screen bg-gray-50 overflow-hidden">
        <Sidebar />
        <div className="flex flex-col flex-1 overflow-hidden">
          <TopBar />
          <main className="flex-1 overflow-y-auto p-6">
            <Routes>
              <Route path="/" element={<Navigate to="/overview" replace />} />
              <Route path="/overview"    element={<Overview />} />
              <Route path="/live"        element={<LiveMonitor />} />
              <Route path="/alerts"      element={<Alerts />} />
              <Route path="/analytics"   element={<Analytics />} />
              <Route path="/plc"         element={<PLCStatus />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/simulation"  element={<SimulationControl />} />
              <Route path="/settings"    element={<Settings />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}
