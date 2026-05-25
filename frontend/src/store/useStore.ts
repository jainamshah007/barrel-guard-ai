// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { create } from 'zustand'

interface Detection {
  id: number
  camera_id: number
  conveyor_line_id: string
  barrel_id: string
  batch_id: string
  object_class: string
  confidence: number
  severity: string
  plc_triggered: boolean
  created_at: string
}

interface Notification {
  id: number
  severity: string
  object_class: string
  line_id: string
  barrel_id: string
  confidence: number
  message: string
  channel: string
  sent_at: string
}

interface PLCState {
  [lineId: string]: {
    status: string
    stopped_at: string | null
  }
}

interface StoreState {
  detections: Detection[]
  notifications: Notification[]
  plcStatus: PLCState
  addDetection: (d: Detection) => void
  addNotification: (n: Notification) => void
  setPLCStatus: (s: PLCState) => void
  clearDetections: () => void
}

export const useStore = create<StoreState>((set) => ({
  detections: [],
  notifications: [],
  plcStatus: {},

  addDetection: (d) =>
    set((state) => ({
      detections: [d, ...state.detections].slice(0, 100)
    })),

  addNotification: (n) =>
    set((state) => ({
      notifications: [n, ...state.notifications].slice(0, 50)
    })),

  setPLCStatus: (s) =>
    set(() => ({ plcStatus: s })),

  clearDetections: () => set({ detections: [] })
}))
