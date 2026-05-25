// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

export default function Settings() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        🛠️ Settings
      </h1>

      <div className="bg-white rounded-xl border border-gray-200
        shadow-sm p-6 space-y-4">
        <h2 className="text-base font-semibold text-gray-700">
          System Information
        </h2>

        <div className="space-y-3 text-sm">
          {[
            ['Platform',   'BARREL-GUARD AI'],
            ['Version',    '1.0.0'],
            ['Copyright',  '© 2024 Jainam K Shah'],
            ['License',    'All Rights Reserved'],
            ['Backend',    'FastAPI + PostgreSQL'],
            ['Frontend',   'React + Vite + Tailwind'],
            ['Deployment', 'Docker Compose']
          ].map(([label, value]) => (
            <div key={label}
              className="flex items-center justify-between
              py-2 border-b border-gray-100">
              <span className="text-gray-500 font-medium">{label}</span>
              <span className="text-gray-800">{value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
