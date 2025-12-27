/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        parchment: {
          50: '#fdfbf7',
          100: '#f9f5ed',
          200: '#f3ebe0',
          300: '#e8dcc9',
          400: '#d9c8ac',
          500: '#c9b390',
          600: '#b89d76',
        },
        ink: {
          800: '#1c1917',
          900: '#0c0a09',
        },
        cinnabar: {
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
        },
      },
      fontFamily: {
        serif: ['Noto Serif', 'Merriweather', 'serif'],
        chinese: ['Noto Serif SC', 'Ma Shan Zheng', 'ZCOOL KuaiLe', 'serif'],
        kaiti: ['Kaiti', 'STKaiti', 'KaiTi', 'serif'],
      },
      backgroundImage: {
        'paper-texture': "url('data:image/svg+xml,%3Csvg width=\"100\" height=\"100\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cfilter id=\"noise\"%3E%3CfeTurbulence type=\"fractalNoise\" baseFrequency=\"0.9\" numOctaves=\"4\" /%3E%3C/filter%3E%3Crect width=\"100\" height=\"100\" filter=\"url(%23noise)\" opacity=\"0.05\" /%3E%3C/svg%3E')",
      },
      boxShadow: {
        'scroll': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06), inset 0 2px 4px rgba(255, 255, 255, 0.5)',
      },
    },
  },
  plugins: [],
}

