// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useStore } from '../store/useStore'
import AlertBadge from '../components/Common/AlertBadge'

export default function Alerts() {
  const detections = useStore((s) => s.detections)

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        🚨 Alerts
      </h1>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div className="px-5 py-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-600">
            Total: {detections.length} detections
          </span>
        </div>

        {detections.length === 0 ? (
          <div className="p-8 text-center text-gray-400 text-sm">
            No alerts yet. System is monitoring...
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {detections.map((d) => (
              <div key={d.id}
                className="flex items-center justify-between
                px-5 py-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-center gap-4">
                  <AlertBadge severity={d.severity} />
                  <div>
                    <div className="text-sm font-semibold text-gray-800">
                      {d.object_class.replace(/_/g, ' ').toUpperCase()}
                    </div>
                    <div className="text-xs text-gray-400 mt-0.5">
                      {d.conveyor_line_id} | Barrel: {d.barrel_id}
                      | Batch: {d.batch_id}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-700">
                    {(d.confidence * 100).toFixed(1)}%
                  </div>
                  <div className="text-xs text-gray-400">
                    {d.plc_triggered ? '⛔ PLC Triggered' : '—'}
                  </div>
                  <div className="text-xs text-gray-300 mt-0.5">
                    {new Date(d.created_at).toLocaleTimeString()}
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
