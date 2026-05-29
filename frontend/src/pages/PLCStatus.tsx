// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useState } from 'react'
import axios from 'axios'
import { useStore } from '../store/useStore'
import { API_BASE } from '../App'

export default function PLCStatus() {
  const plcStatus = useStore((s) => s.plcStatus)
  const [loading, setLoading] = useState<string | null>(null)

  const handleStop = async (lineId: string) => {
    setLoading(lineId)
    try {
      await axios.post(`${API_BASE}/api/v1/plc/stop`, {
        line_id: lineId,
        operator: 'OPERATOR',
        notes: 'Manual stop from dashboard'
      })
    } catch (e) {
      console.error(e)
    }
    setLoading(null)
  }

  const handleResume = async (lineId: string) => {
    setLoading(lineId)
    try {
      await axios.post(`${API_BASE}/api/v1/plc/resume`, {
        line_id: lineId,
        operator: 'OPERATOR'
      })
    } catch (e) {
      console.error(e)
    }
    setLoading(null)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        ⚙️ PLC Status
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {['LINE_A', 'LINE_B'].map((lineId) => {
          const state = plcStatus[lineId]
          const isRunning = !state || state.status === 'running'

          return (
            <div key={lineId}
              className="bg-white rounded-xl border border-gray-200
              shadow-sm p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-gray-800">
                  {lineId.replace('_', ' ')}
                </h2>
                <span className={`px-3 py-1 rounded-full text-sm
                  font-bold ${isRunning
                    ? 'bg-green-100 text-green-700'
                    : 'bg-red-100 text-red-700'
                  }`}>
                  {isRunning ? 'RUNNING' : 'STOPPED'}
                </span>
              </div>

              {state?.stopped_at && (
                <div className="text-xs text-gray-400">
                  Stopped at: {new Date(state.stopped_at).toLocaleTimeString()}
                </div>
              )}

              <div className="flex gap-3">
                <button
                  onClick={() => handleStop(lineId)}
                  disabled={!isRunning || loading === lineId}
                  className="flex-1 py-2 rounded-lg text-sm font-semibold
                    bg-red-600 text-white hover:bg-red-700
                    disabled:opacity-40 disabled:cursor-not-allowed
                    transition-colors"
                >
                  ⛔ Stop Line
                </button>
                <button
                  onClick={() => handleResume(lineId)}
                  disabled={isRunning || loading === lineId}
                  className="flex-1 py-2 rounded-lg text-sm font-semibold
                    bg-green-600 text-white hover:bg-green-700
                    disabled:opacity-40 disabled:cursor-not-allowed
                    transition-colors"
                >
                  ▶️ Resume Line
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}