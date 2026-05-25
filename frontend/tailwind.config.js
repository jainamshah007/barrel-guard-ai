// =============================================================
// BARREL-GUARD AI — Foreign Object Detection Platform
// Copyright (c) 2024 Jainam K Shah. All Rights Reserved.
// Unauthorized copying, modification, or distribution of
// this file, via any medium, is strictly prohibited.
// =============================================================

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50:  '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          900: '#1e3a5f'
        },
        success: '#16a34a',
        warning: '#d97706',
        danger:  '#dc2626'
      }
    }
  },
  plugins: []
}
