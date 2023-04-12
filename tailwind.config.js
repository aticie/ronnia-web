/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "red": "#da0037",
        "dark": "#101010"
      }
    },
  },
  plugins: [],
}

