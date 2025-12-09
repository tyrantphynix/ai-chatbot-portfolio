/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        perplexity: {
          dark: '#0a0a0a',
          gray: '#1f1f1f',
          blue: '#3b82f6',
          text: '#e5e5e5',
          subtext: '#a3a3a3',
        }
      },
      boxShadow: {
        'glow': '0 0 20px rgba(59, 130, 246, 0.15)',
        'glow-strong': '0 0 30px rgba(59, 130, 246, 0.3)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
