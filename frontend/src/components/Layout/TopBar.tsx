// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useStore } from '../../store/useStore'

export default function TopBar() {
  const detections    = useStore((s) => s.detections)
  const notifications = useStore((s) => s.notifications)

  return (
    <header className="bg-white border-b border-gray-200
      px-6 py-3 flex items-center justify-between shadow-sm">
      {/* Left */}
      <div className="flex items-center gap-3">
        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
        <span className="text-sm text-gray-600 font-medium">
          System Online
        </span>
      </div>

      {/* Center */}
      <div className="text-sm font-semibold text-gray-700">
        BARREL-GUARD AI — Industrial FOD Platform
      </div>

      {/* Right */}
      <div className="flex items-center gap-4 text-sm text-gray-500">
        <span>
          🚨 <strong className="text-red-600">{detections.length}</strong> Detections
        </span>
        <span>
          🔔 <strong className="text-blue-600">{notifications.length}</strong> Alerts
        </span>
        <span className="text-gray-300">|</span>
        <span className="text-xs text-gray-400">
          {new Date().toLocaleDateString()}
        </span>
      </div>
    </header>
  )
}
