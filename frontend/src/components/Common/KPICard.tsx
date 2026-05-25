// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

interface KPICardProps {
  title: string
  value: string | number
  subtitle?: string
  color?: string
  icon?: React.ReactNode
}

export default function KPICard({
  title, value, subtitle, color = '#2563eb', icon
}: KPICardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-500">{title}</span>
        {icon && (
          <span style={{ color }} className="text-xl">{icon}</span>
        )}
      </div>
      <div className="text-3xl font-bold" style={{ color }}>
        {value}
      </div>
      {subtitle && (
        <div className="text-xs text-gray-400 mt-1">{subtitle}</div>
      )}
    </div>
  )
}
