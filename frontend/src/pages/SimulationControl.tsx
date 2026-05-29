// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useState } from 'react'
import axios from 'axios'
import { API_BASE } from '../App'

const OBJECT_CLASSES = [
  'hard_helmet', 'glove', 'face_mask',
  'key', 'wallet', 'tool', 'cloth', 'bottle'
]

export default function SimulationControl() {
  const [autoMode, setAutoMode] = useState(true)
  const [cameraId, setCameraId] = useState(0)
  const [objClass, setObjClass] = useState(OBJECT_CLASSES[0])
  const [status, setStatus]     = useState('')

  const toggleAuto = async () => {
    try {
      await axios.post(`${API_BASE}/api/v1/simulation/config`, {
        auto_mode: !autoMode
      })
      setAutoMode(!autoMode)
      setStatus(`Auto mode ${!autoMode ? 'enabled' : 'disabled'}`)
    } catch {
      setStatus('❌ Error updating config')
    }
  }

  const injectManual = async () => {
    try {
      await axios.post(`${API_BASE}/api/v1/simulation/inject`, {
        camera_id: cameraId,
        object_class: objClass
      })
      setStatus(`✅ Injected: ${objClass} on Camera ${cameraId}`)
    } catch {
      setStatus('❌ Injection failed')
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        🎮 Simulation Control
      </h1>

      {/* Auto Mode */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
        <h2 className="text-base font-semibold text-gray-700 mb-4">
          Auto Simulation Mode
        </h2>
        <div className="flex items-center gap-4">
          <span className={`text-sm font-medium ${
            autoMode ? 'text-green-600' : 'text-gray-400'
          }`}>
            {autoMode ? '🟢 Auto Mode ON' : '⚪ Auto Mode OFF'}
          </span>
          <button
            onClick={toggleAuto}
            className={`px-4 py-2 rounded-lg text-sm font-semibold
              text-white transition-colors ${
              autoMode
                ? 'bg-red-500 hover:bg-red-600'
                : 'bg-green-500 hover:bg-green-600'
            }`}
          >
            {autoMode ? 'Disable Auto' : 'Enable Auto'}
          </button>
        </div>
      </div>

      {/* Manual Inject */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
        <h2 className="text-base font-semibold text-gray-700 mb-4">
          Manual Object Injection
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="text-xs text-gray-500 font-medium mb-1 block">
              Camera
            </label>
            <select
              value={cameraId}
              onChange={(e) => setCameraId(Number(e.target.value))}
              className="w-full border border-gray-200 rounded-lg
                px-3 py-2 text-sm focus:outline-none focus:ring-2
                focus:ring-blue-300"
            >
              <option value={0}>Camera 1 – Line A</option>
              <option value={1}>Camera 2 – Line B</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-gray-500 font-medium mb-1 block">
              Object Class
            </label>
            <select
              value={objClass}
              onChange={(e) => setObjClass(e.target.value)}
              className="w-full border border-gray-200 rounded-lg
                px-3 py-2 text-sm focus:outline-none focus:ring-2
                focus:ring-blue-300"
            >
              {OBJECT_CLASSES.map((c) => (
                <option key={c} value={c}>
                  {c.replace(/_/g, ' ')}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={injectManual}
              className="w-full py-2 rounded-lg text-sm font-semibold
                bg-blue-600 text-white hover:bg-blue-700 transition-colors"
            >
              ⚡ Inject Now
            </button>
          </div>
        </div>

        {status && (
          <div className="mt-4 text-sm text-blue-700 bg-blue-50
            rounded-lg px-4 py-2 border border-blue-100">
            {status}
          </div>
        )}
      </div>
    </div>
  )
}
