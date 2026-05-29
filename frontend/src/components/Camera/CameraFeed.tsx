// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useEffect, useRef } from 'react'
import { useStore } from '../../store/useStore'

interface CameraFeedProps {
  cameraId: number
  name: string
  lineId: string
}

export default function CameraFeed({ cameraId, name, lineId }: CameraFeedProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const frameRef  = useRef(0)
  const posRef    = useRef(0)

  const detections = useStore((s) =>
    s.detections.filter((d) => d.camera_id === cameraId).slice(0, 1)
  )
  const plcStatus = useStore((s) => s.plcStatus)

  const isRunning = !plcStatus[lineId] || plcStatus[lineId].status === 'running'
  const latest    = detections[0]

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const W = canvas.width
    const H = canvas.height

    const draw = () => {
      // Background
      ctx.fillStyle = '#1f2937'
      ctx.fillRect(0, 0, W, H)

      // Conveyor belt base
      ctx.fillStyle = '#374151'
      ctx.fillRect(0, H * 0.55, W, H * 0.3)

      // Moving belt stripes
      if (isRunning) posRef.current = (posRef.current + 2) % 40

      for (let x = -40 + posRef.current; x < W + 40; x += 40) {
        ctx.fillStyle = '#4b5563'
        ctx.fillRect(x, H * 0.55, 20, H * 0.3)
      }

      // Belt border lines
      ctx.strokeStyle = '#6b7280'
      ctx.lineWidth = 2
      ctx.beginPath()
      ctx.moveTo(0, H * 0.55)
      ctx.lineTo(W, H * 0.55)
      ctx.stroke()
      ctx.beginPath()
      ctx.moveTo(0, H * 0.85)
      ctx.lineTo(W, H * 0.85)
      ctx.stroke()

      // Barrel
      const barrelX = W * 0.4
      const barrelY = H * 0.3
      const barrelW = 60
      const barrelH = 70

      // Barrel body
      ctx.fillStyle = latest ? '#dc2626' : '#2563eb'
      ctx.beginPath()
      ctx.roundRect(barrelX, barrelY, barrelW, barrelH, 6)
      ctx.fill()

      // Barrel stripes
      ctx.strokeStyle = latest ? '#991b1b' : '#1d4ed8'
      ctx.lineWidth = 3
      for (let i = 1; i <= 3; i++) {
        ctx.beginPath()
        ctx.moveTo(barrelX, barrelY + (barrelH / 4) * i)
        ctx.lineTo(barrelX + barrelW, barrelY + (barrelH / 4) * i)
        ctx.stroke()
      }

      // Barrel label
      ctx.fillStyle = '#ffffff'
      ctx.font = 'bold 10px sans-serif'
      ctx.textAlign = 'center'
      ctx.fillText('BARREL', barrelX + barrelW / 2, barrelY + barrelH / 2)

      // Object inside barrel if detected
      if (latest) {
        ctx.fillStyle = '#fbbf24'
        ctx.font = 'bold 9px sans-serif'
        ctx.fillText(
          latest.object_class.replace(/_/g, ' ').toUpperCase(),
          barrelX + barrelW / 2,
          barrelY + barrelH / 2 + 14
        )

        // Alert border flash
        ctx.strokeStyle = '#ef4444'
        ctx.lineWidth = 3
        ctx.strokeRect(2, 2, W - 4, H - 4)
      }

      // Rollers
      ctx.fillStyle = '#9ca3af'
      for (const rx of [20, W / 2, W - 20]) {
        ctx.beginPath()
        ctx.arc(rx, H * 0.7, 8, 0, Math.PI * 2)
        ctx.fill()
      }

      // Status text
      ctx.fillStyle = isRunning ? '#4ade80' : '#f87171'
      ctx.font = 'bold 11px sans-serif'
      ctx.textAlign = 'left'
      ctx.fillText(
        isRunning ? '● RUNNING' : '■ STOPPED',
        8, 16
      )

      frameRef.current = requestAnimationFrame(draw)
    }

    frameRef.current = requestAnimationFrame(draw)
    return () => cancelAnimationFrame(frameRef.current)
  }, [isRunning, latest])

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2
        bg-gray-50 border-b border-gray-200">
        <span className="text-sm font-semibold text-gray-700">{name}</span>
        <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
          isRunning
            ? 'bg-green-100 text-green-700'
            : 'bg-red-100 text-red-700'
        }`}>
          {isRunning ? '🟢 RUNNING' : '🔴 STOPPED'}
        </span>
      </div>

      {/* Animated Canvas */}
      <canvas
        ref={canvasRef}
        width={320}
        height={200}
        className="w-full"
      />

      {/* Detection overlay */}
      {latest && (
        <div className="bg-red-600 text-white text-xs px-3 py-1.5
          flex items-center justify-between">
          <span>⚠️ {latest.object_class.replace(/_/g, ' ').toUpperCase()} — Barrel {latest.barrel_id}</span>
          <span>{(latest.confidence * 100).toFixed(0)}% conf</span>
        </div>
      )}

      {/* Status bar */}
      <div className="px-4 py-2 flex items-center justify-between
        bg-gray-50 border-t border-gray-100">
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