const { default: daisyui } = require('daisyui');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/**/*.html",
    "../*.py",
    "../**/*.py",
  ],
  daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/theming/themes")["[data-theme=light]"],
          "--rounded-btn": "none",
        }
      }
    ]
  },
  theme: {
    extend: {
      fontSize: {
        base: ['0.875rem', {lineHeight: '1.25rem'}]
      }
    },
  },
  plugins: [
    require("daisyui"),
  ],
}

