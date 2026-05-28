// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useStore } from '../store/useStore';

export default function Notifications() {
  const notifications = useStore((s) => s.notifications);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        🔔 Notifications
      </h1>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        {notifications.length === 0 ? (
          <div className="p-8 text-center text-gray-400 text-sm">
            No notifications yet...
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {notifications.map((n, i) => (
              <div
                key={i}
                className="px-5 py-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                      n.read
                        ? 'bg-gray-100 text-gray-500'
                        : 'bg-blue-100 text-blue-700'
                    }`}>
                      {n.read ? 'READ' : 'NEW'}
                    </span>
                    <div>
                      <div className="text-sm font-semibold text-gray-800">
                        {n.message}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        {n.object_class.replace(/_/g, ' ').toUpperCase()} | {n.camera_name}
                      </div>
                    </div>
                  </div>
                  <div className="text-xs text-gray-300 whitespace-nowrap">
                    {new Date(n.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}