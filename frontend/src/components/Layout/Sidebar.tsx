// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { NavLink } from 'react-router-dom'

const navItems = [
  { path: '/overview',      label: 'Overview',         icon: '🏠' },
  { path: '/live',          label: 'Live Monitor',      icon: '📷' },
  { path: '/alerts',        label: 'Alerts',            icon: '🚨' },
  { path: '/analytics',     label: 'Analytics',         icon: '📊' },
  { path: '/plc',           label: 'PLC Status',        icon: '⚙️'  },
  { path: '/notifications', label: 'Notifications',     icon: '🔔' },
  { path: '/simulation',    label: 'Simulation',        icon: '🎮' },
  { path: '/settings',      label: 'Settings',          icon: '🛠️'  }
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-gray-200
      flex flex-col shadow-sm">
      {/* Logo */}
      <div className="px-6 py-5 border-b border-gray-200">
        <div className="text-lg font-bold text-blue-900">
          🛡️ BARREL-GUARD AI
        </div>
        <div className="text-xs text-gray-400 mt-0.5">
          Foreign Object Detection
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg
              text-sm font-medium transition-colors
              ${isActive
                ? 'bg-blue-50 text-blue-700 border border-blue-100'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-6 py-4 border-t border-gray-200">
        <div className="text-xs text-gray-400">
          © 2024 Jainam K Shah
        </div>
        <div className="text-xs text-gray-300">All Rights Reserved</div>
      </div>
    </aside>
  )
}