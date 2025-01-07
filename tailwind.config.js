/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Percorso ai tuoi file HTML Flask
    './static/js/**/*.js',   // Percorso ai file JavaScript (opzionale)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
