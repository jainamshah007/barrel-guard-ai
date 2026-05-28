/*
 * BARREL-GUARD AI — Foreign Object Detection Platform
 * Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
 */

import { create } from 'zustand';

export interface Detection {
  id: number;
  camera_id: number;
  camera_name: string;
  object_class: string;
  confidence: number;
  timestamp: string;
  line_id: string;
  barrel_id?: string;
  batch_id?: string;
}

export interface NotificationItem {
  id: number;
  title: string;
  message: string;
  severity: string;
  camera_id?: number;
  object_class?: string;
  is_read: boolean;
  timestamp: string;
}

export interface PLCLine {
  line_id: string;
  name: string;
  status: string;
  stopped_at?: string;
  reason?: string;
}

export interface StoreState {
  detections: Detection[];
  notifications: NotificationItem[];
  plcStatus: Record<string, PLCLine>;
  addDetection: (d: Detection) => void;
  addNotification: (n: NotificationItem) => void;
  setPLCStatus: (line: PLCLine) => void;
  markAllRead: () => void;
}

export const useStore = create<StoreState>((set) => ({
  detections: [],
  notifications: [],
  plcStatus: {},

  addDetection: (d) =>
    set((state) => ({
      detections: [d, ...state.detections].slice(0, 100),
    })),

  addNotification: (n) =>
    set((state) => ({
      notifications: [n, ...state.notifications].slice(0, 50),
    })),

  setPLCStatus: (line) =>
    set((state) => ({
      plcStatus: {
        ...state.plcStatus,
        [line.line_id]: line,
      },
    })),

  markAllRead: () =>
    set((state) => ({
      notifications: state.notifications.map((n) => ({ ...n, is_read: true })),
    })),
}));
