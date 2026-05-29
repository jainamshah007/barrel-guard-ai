// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useEffect, useState, useCallback, useRef } from 'react'
import axios from 'axios'
import { useStore } from '../store/useStore'
import KPICard from '../components/Common/KPICard'
import { API_BASE } from '../App'

const OBJECT_SYMBOLS: Record<string, string> = {
  hard_helmet : '⛑️',
  glove       : '🧤',
  face_mask   : '😷',
  key         : '🔑',
  wallet      : '👛',
  tool        : '🔧',
  cloth       : '🧣',
  bottle      : '🍶',
}

export default function Overview() {
  const detections      = useStore((s) => s.detections)
  const plcStatus       = useStore((s) => s.plcStatus)
  const addDetection    = useStore((s) => s.addDetection)
  const setAllPLCStatus = useStore((s) => s.setAllPLCStatus)
  const [loading, setLoading]     = useState(false)
  const [lastFetch, setLastFetch] = useState('')
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const fetchAll = useCallback(() => {
    setLoading(true)

    // Fetch detections
    axios.get(`${API_BASE}/api/v1/detections/recent`)
      .then((res) => {
        if (Array.isArray(res.data)) {
          res.data.forEach((d: any) => addDetection(d))
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))

    // Fetch PLC status
    axios.get(`${API_BASE}/api/v1/plc/status`)
      .then((res) => {
        if (res.data?.lines) setAllPLCStatus(res.data.lines)
      })
      .catch(() => {})

    setLastFetch(new Date().toLocaleTimeString())
  }, [addDetection, setAllPLCStatus])

  // Fetch on mount
  useEffect(() => {
    fetchAll()
  }, [fetchAll])

  // Auto-refresh every 10 seconds
  useEffect(() => {
    timerRef.current = setInterval(fetchAll, 10000)
    return () => {
      if (timerRef.current) clearInterval(timerRef.current)
    }
  }, [fetchAll])

  // Re-fetch when user returns to tab
  useEffect(() => {
    const onVisible = () => {
      if (document.visibilityState === 'visible') fetchAll()
    }
    document.addEventListener('visibilitychange', onVisible)
    return () => document.removeEventListener('visibilitychange', onVisible)
  }, [fetchAll])

  const stoppedLines = Object.values(plcStatus).filter(
    (l) => l.status === 'stopped'
  ).length

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">
          📊 System Overview
        </h1>
        <div className="flex items-center gap-3">
          {lastFetch && (
            <span className="text-xs text-gray-400">
              Updated: {lastFetch}
            </span>
          )}
          <button
            onClick={fetchAll}
            disabled={loading}
            className="text-xs px-3 py-1.5 rounded-lg bg-blue-50
              text-blue-600 border border-blue-200 hover:bg-blue-100
              disabled:opacity-50 transition-colors font-medium"
          >
            {loading ? '⏳' : '🔄 Refresh'}
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total Detections"
          value={detections.length}
          subtitle="Since session start"
          color="#2563eb"
          icon="🔍"
        />
        <KPICard
          title="Foreign Objects"
          value={detections.length}
          subtitle="All detections are alerts"
          color="#dc2626"
          icon="🚨"
        />
        <KPICard
          title="Lines Stopped"
          value={stoppedLines}
          subtitle="Out of 2 conveyor lines"
          color="#d97706"
          icon="⛔"
        />
        <KPICard
          title="Lines Running"
          value={2 - stoppedLines}
          subtitle="Active conveyor lines"
          color="#16a34a"
          icon="✅"
        />
      </div>

      {/* PLC Status */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
        <h2 className="text-base font-semibold text-gray-700 mb-4">
          ⚙️ Conveyor Line Status
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {['line_a', 'line_b'].map((lineId) => {
            const state     = plcStatus[lineId]
            const isRunning = !state || state.status === 'running'
            return (
              <div
                key={lineId}
                className="flex items-center justify-between p-4
                  rounded-lg border border-gray-100 bg-gray-50"
              >
                <span className="font-medium text-gray-700">
                  {lineId === 'line_a' ? '🔵 Line A' : '🟣 Line B'}
                </span>
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                  isRunning
                    ? 'bg-green-100 text-green-700'
                    : 'bg-red-100 text-red-700'
                }`}>
                  {isRunning ? '🟢 RUNNING' : '🔴 STOPPED'}
                </span>
              </div>
            )
          })}
        </div>
      </div>

      {/* Recent Detections */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
        <h2 className="text-base font-semibold text-gray-700 mb-4">
          🔍 Recent Detections
        </h2>

        {loading && detections.length === 0 && (
          <div className="text-sm text-gray-400 animate-pulse">
            ⏳ Loading detections...
          </div>
        )}

        {!loading && detections.length === 0 && (
          <div className="text-sm text-gray-400">
            No detections yet. Simulator is running...
          </div>
        )}

        {detections.length > 0 && (
          <div className="space-y-2">
            {detections.slice(0, 8).map((d, i) => (
              <div
                key={d.id ?? i}
                className="flex items-center justify-between p-3
                  rounded-lg border border-gray-100 hover:bg-gray-50"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xl">
                    {OBJECT_SYMBOLS[d.object_class] ?? '⚠️'}
                  </span>
                  <div>
                    <div className="text-sm font-medium text-gray-700">
                      {d.object_class.replace(/_/g, ' ').toUpperCase()}
                    </div>
                    <div className="text-xs text-gray-400">
                      {d.camera_name} — Barrel {d.barrel_id} — {d.line_id}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs font-semibold text-red-600">
                    {(d.confidence * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-gray-400">
                    {new Date(d.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  )
}