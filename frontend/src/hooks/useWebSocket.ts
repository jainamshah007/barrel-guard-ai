/*
 * BARREL-GUARD AI — Foreign Object Detection Platform
 * Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
 */

import { useEffect, useRef } from 'react';
import { useStore } from '../store/useStore';

export const useWebSocket = () => {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const store = useStore();

  const connect = () => {
    const wsUrl = import.meta.env.VITE_WS_URL || 'wss://barrel-guard-ai-production.up.railway.app';
    const clientId = `client-${Date.now()}`;
    const url = `${wsUrl}/ws/${clientId}`;

    console.log(`🔌 Connecting to WebSocket: ${url}`);

    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('✅ WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const { type, payload } = message;

        if (type === 'new_detection') {
          store.addDetection(payload);
        } else if (type === 'notification') {
          store.addNotification(payload);
        } else if (type === 'plc_stop' || type === 'plc_resume' || type === 'plc_status') {
          store.setPLCStatus(type, payload);
        }
      } catch (e) {
        console.error('WebSocket message parse error:', e);
      }
    };

    ws.onerror = () => {
      console.error('❌ WebSocket error');
    };

    ws.onclose = () => {
      console.log('🔄 WebSocket disconnected — reconnecting in 3s...');
      reconnectRef.current = setTimeout(connect, 3000);
    };
  };

  useEffect(() => {
    connect();
    return () => {
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
      if (wsRef.current) wsRef.current.close();
    };
  }, []);
};
