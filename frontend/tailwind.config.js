/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        mono: ["'JetBrains Mono'", "ui-monospace", "SFMono-Regular", "monospace"],
        sans: ["'Inter'", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        console: {
          950: "#0b0f14",
          900: "#111820",
          800: "#182230",
          700: "#22303f",
          600: "#334255",
          400: "#7c8ea3",
          200: "#c7d2de",
        },
        review: "#5eb8ff",
        bug: "#ff6b6b",
        complexity: "#ffb84d",
        performance: "#7ee8a3",
        validation: "#c792ea",
      },
    },
  },
  plugins: [],
};
