module.exports = {
  content: [
    './src/**/*.{html,js,svelte,ts}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1f2937',
        accent: '#fbbf24',
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};
