// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useStore } from '../store/useStore'
import KPICard from '../components/Common/KPICard'
import AlertBadge from '../components/Common/AlertBadge'

export default function Overview() {
  const detections = useStore((s) => s.detections)
  const plcStatus  = useStore((s) => s.plcStatus)

  const highCount   = detections.filter((d) => d.severity === 'HIGH').length
  const stoppedLines = Object.values(plcStatus)
    .filter((l) => l.status === 'STOPPED').length

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        📊 System Overview
      </h1>

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
          title="High Severity"
          value={highCount}
          subtitle="Requires immediate action"
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
      <div className="bg-white rounded-xl border border-gray-200
        shadow-sm p-5">
        <h2 className="text-base font-semibold text-gray-700 mb-4">
          ⚙️ Conveyor Line Status
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {Object.entries(plcStatus).map(([lineId, state]) => (
            <div key={lineId}
              className="flex items-center justify-between
              p-4 rounded-lg border border-gray-100 bg-gray-50">
              <span className="font-medium text-gray-700">{lineId}</span>
              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                state.status === 'RUNNING'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-red-100 text-red-700'
              }`}>
                {state.status}
              </span>
            </div>
          ))}
          {Object.keys(plcStatus).length === 0 && (
            <div className="text-sm text-gray-400 col-span-2">
              Waiting for PLC status...
            </div>
          )}
        </div>
      </div>

      {/* Recent Detections */}
      <div className="bg-white rounded-xl border border-gray-200
        shadow-sm p-5">
        <h2 className="text-base font-semibold text-gray-700 mb-4">
          🔍 Recent Detections
        </h2>
        {detections.length === 0 ? (
          <div className="text-sm text-gray-400">
            No detections yet. Simulator is running...
          </div>
        ) : (
          <div className="space-y-2">
            {detections.slice(0, 8).map((d) => (
              <div key={d.id}
                className="flex items-center justify-between
                p-3 rounded-lg border border-gray-100 hover:bg-gray-50">
                <div className="flex items-center gap-3">
                  <AlertBadge severity={d.severity} />
                  <span className="text-sm font-medium text-gray-700">
                    {d.object_class.replace(/_/g, ' ').toUpperCase()}
                  </span>
                  <span className="text-xs text-gray-400">
                    {d.conveyor_line_id} — Barrel {d.barrel_id}
                  </span>
                </div>
                <div className="text-xs text-gray-400">
                  {(d.confidence * 100).toFixed(0)}% confidence
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
