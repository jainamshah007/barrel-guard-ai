 
// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useEffect } from 'react'
import { useStore } from '../store/useStore'

export function useWebSocket() {
  const { addDetection, addNotification, setPLCStatus } = useStore()

  useEffect(() => {
    const clientId = `client-${Date.now()}`
    const wsUrl = `ws://${window.location.hostname}:8000/ws/${clientId}`
    const ws = new WebSocket(wsUrl)

    ws.onopen = () => console.log('WebSocket connected')

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data)
        if (msg.type === 'new_detection')  addDetection(msg.data)
        if (msg.type === 'notification')   addNotification(msg.data)
        if (msg.type === 'plc_status')     setPLCStatus(msg.data)
        if (msg.type === 'plc_stop')       setPLCStatus(msg.data)
        if (msg.type === 'plc_resume')     setPLCStatus(msg.data)
      } catch (e) {
        console.error('WS parse error', e)
      }
    }

    ws.onerror = (e) => console.error('WebSocket error', e)
    ws.onclose = () => console.log('WebSocket disconnected')

    return () => ws.close()
  }, [])
}
