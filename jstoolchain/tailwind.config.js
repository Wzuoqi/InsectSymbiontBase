/** @type {import('tailwindcss').Config} */

import { addDynamicIconSelectors } from '@iconify/tailwind'

module.exports = {
  content: ["../templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'regal-blue': '#243c5a',
        'kabuli': {
          50: '#eff8ff',
          100: '#dfefff',
          200: '#b7e1ff',
          300: '#77caff',
          400: '#2fb0ff',
          500: '#0395f4',
          600: '#0075d1',
          700: '#005da9',
          800: '#015697',
          900: '#074273',
          950: '#052a4c',
        },
        'tahiti': {
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#22d3ee',
          500: '#06b6d4',
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63',
        },

      },
      backgroundImage: theme => ({
        'gradient-endeavour': 'linear-gradient(to right, #eff8ff, #2fb0ff, #0395f4, #005da9, #052a4c)',
      }),
    },
  },
  plugins: [
    addDynamicIconSelectors()
  ],
}

