// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

interface AlertBadgeProps {
  severity: string
}

export default function AlertBadge({ severity }: AlertBadgeProps) {
  const styles: Record<string, string> = {
    HIGH:   'bg-red-100 text-red-700 border border-red-200',
    MEDIUM: 'bg-yellow-100 text-yellow-700 border border-yellow-200',
    LOW:    'bg-green-100 text-green-700 border border-green-200'
  }

  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold
      ${styles[severity] || styles['LOW']}`}>
      {severity}
    </span>
  )
}
