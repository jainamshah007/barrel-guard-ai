// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// =============================================================

import { useStore } from '../store/useStore'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from 'recharts'

const COLORS = ['#2563eb', '#dc2626', '#16a34a', '#d97706',
                '#7c3aed', '#0891b2', '#be185d', '#065f46']

export default function Analytics() {
  const detections = useStore((s) => s.detections)

  // Count by object class
  const classCounts = detections.reduce<Record<string, number>>((acc, d) => {
    acc[d.object_class] = (acc[d.object_class] || 0) + 1
    return acc
  }, {})

  const barData = Object.entries(classCounts).map(([name, count]) => ({
    name: name.replace(/_/g, ' '),
    count
  }))

  // Count by line
  const lineCounts = detections.reduce<Record<string, number>>((acc, d) => {
    acc[d.conveyor_line_id] = (acc[d.conveyor_line_id] || 0) + 1
    return acc
  }, {})

  const pieData = Object.entries(lineCounts).map(([name, value]) => ({
    name, value
  }))

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">
        📊 Analytics
      </h1>

      {detections.length === 0 ? (
        <div className="bg-white rounded-xl border border-gray-200
          shadow-sm p-12 text-center text-gray-400">
          No data yet. Waiting for detections...
        </div>
      ) : (
        <>
          {/* Bar Chart */}
          <div className="bg-white rounded-xl border border-gray-200
            shadow-sm p-5">
            <h2 className="text-base font-semibold text-gray-700 mb-4">
              Detections by Object Class
            </h2>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#2563eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Pie Chart */}
          <div className="bg-white rounded-xl border border-gray-200
            shadow-sm p-5">
            <h2 className="text-base font-semibold text-gray-700 mb-4">
              Detections by Conveyor Line
            </h2>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {pieData.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  )
}
