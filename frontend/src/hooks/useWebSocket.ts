// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// Unauthorized copying, modification, or distribution is
// strictly prohibited without explicit written permission.
// =============================================================

import { useEffect, useRef, useCallback } from 'react'
import { useStore } from '../store/useStore'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export const useWebSocket = () => {
  const wsRef = useRef<WebSocket | null>(null)
  const addDetection = useStore((state) => state.addDetection)
  const addNotification = useStore((state) => state.addNotification)
  const setPLCStatus = useStore((state) => state.setPLCStatus)

  const connect = useCallback(() => {
    const clientId = `client-${Date.now()}`
    const ws = new WebSocket(`${WS_URL}/ws/${clientId}`)

    ws.onopen = () => {
      console.log('✅ WebSocket connected')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.type === 'new_detection') {
          addDetection(data.payload)
        }

        if (data.type === 'notification') {
          addNotification(data.payload)
        }

        if (
          data.type === 'plc_status' ||
          data.type === 'plc_stop' ||
          data.type === 'plc_resume'
        ) {
          setPLCStatus(data.payload)
        }

      } catch (e) {
        console.error('❌ WS parse error', e)
      }
    }

    ws.onclose = () => {
      console.log('🔄 WebSocket disconnected — reconnecting in 3s...')
      setTimeout(connect, 3000)
    }

    ws.onerror = (error) => {
      console.error('❌ WebSocket error', error)
      ws.close()
    }

    wsRef.current = ws
  }, [addDetection, addNotification, setPLCStatus])

  useEffect(() => {
    connect()
    return () => {
      wsRef.current?.close()
    }
  }, [connect])

  return wsRef
}