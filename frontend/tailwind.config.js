/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx,svelte}",
  ],
  theme: {
    extend: {
      colors: {
        "red-primary": "#da0037",
        "dark": "#101010"
      }
    },
  },
  plugins: [],
}
