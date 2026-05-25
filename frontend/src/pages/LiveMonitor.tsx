// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import CameraFeed from '../components/Camera/CameraFeed'

const CAMERAS = [
  { id: 1, name: 'Camera 1 – Line A', lineId: 'LINE_A' },
  { id: 2, name: 'Camera 2 – Line B', lineId: 'LINE_B' }
]

export default function LiveMonitor() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        📷 Live Monitor
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {CAMERAS.map((cam) => (
          <CameraFeed
            key={cam.id}
            cameraId={cam.id}
            name={cam.name}
            lineId={cam.lineId}
          />
        ))}
      </div>
    </div>
  )
}
