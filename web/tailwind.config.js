/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          'tan': '#fcf1e3',
          'ketchup': '#d83c23',
          'silver': '#6e96a4',
        }
      },
    },
    plugins: [],
  }