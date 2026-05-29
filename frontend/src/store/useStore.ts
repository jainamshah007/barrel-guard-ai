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
  barrel_id: string;
  batch_id: string;
  bbox?: number[];
}

export interface NotificationItem {
  id: number;
  message: string;
  object_class: string;
  camera_name: string;
  timestamp: string;
  read: boolean;
}

export interface PLCLineStatus {
  status: 'running' | 'stopped';
  stopped_at: string | null;
}

interface StoreState {
  detections: Detection[];
  notifications: NotificationItem[];
  plcStatus: Record<string, PLCLineStatus>;
  autoMode: boolean;
  addDetection: (d: Detection) => void;
  addNotification: (n: NotificationItem) => void;
  setPLCStatus: (lineId: string, status: PLCLineStatus) => void;
  markAllRead: () => void;
  setAutoMode: (val: boolean) => void;
}

export const useStore = create<StoreState>((set) => ({
  detections: [],
  notifications: [],
  plcStatus: {},
  autoMode: true,

  addDetection: (d) =>
    set((state) => ({
      detections: [d, ...state.detections].slice(0, 100),
    })),

  addNotification: (n) =>
    set((state) => ({
      notifications: [n, ...state.notifications].slice(0, 50),
    })),

  setPLCStatus: (lineId, status) =>
    set((state) => ({
      plcStatus: { ...state.plcStatus, [lineId]: status },
    })),

  markAllRead: () =>
    set((state) => ({
      notifications: state.notifications.map((n) => ({ ...n, read: true })),
    })),

  setAutoMode: (val) =>
    set({ autoMode: val }),
}));