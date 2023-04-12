/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        red: {
          DEFAULT: "#da0037",
        },
        dark: {
          DEFAULT: "#101010"
        }
      }
    },
  },
  plugins: [],
}

