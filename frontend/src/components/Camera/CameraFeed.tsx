// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useStore } from '../../store/useStore'

interface CameraFeedProps {
  cameraId: number
  name: string
  lineId: string
}

export default function CameraFeed({ cameraId, name, lineId }: CameraFeedProps) {
  const detections = useStore((s) =>
    s.detections.filter((d) => d.camera_id === cameraId).slice(0, 1)
  )
  const latest = detections[0]

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      {/* Camera Header */}
      <div className="flex items-center justify-between px-4 py-2
        bg-gray-50 border-b border-gray-200">
        <span className="text-sm font-semibold text-gray-700">{name}</span>
        <span className="text-xs text-gray-400">{lineId}</span>
      </div>

      {/* Simulated Feed */}
      <div className="relative bg-gray-800 h-48 flex items-center justify-center">
        <div className="text-gray-500 text-sm">📷 Simulated Feed</div>

        {latest && (
          <div className="absolute top-2 left-2 right-2
            bg-red-600 text-white text-xs rounded px-2 py-1">
            ⚠️ {latest.object_class.replace('_', ' ').toUpperCase()}
            — Barrel {latest.barrel_id}
            — {(latest.confidence * 100).toFixed(0)}%
          </div>
        )}
      </div>

      {/* Status Bar */}
      <div className="px-4 py-2 flex items-center justify-between">
        <span className={`text-xs font-medium ${
          latest ? 'text-red-600' : 'text-green-600'
        }`}>
          {latest ? '🔴 Object Detected' : '🟢 Clear'}
        </span>
        <span className="text-xs text-gray-400">
          {latest
            ? new Date(latest.timestamp).toLocaleTimeString()
            : 'Monitoring...'}
        </span>
      </div>
    </div>
  )
}
