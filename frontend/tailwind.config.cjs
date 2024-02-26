/** @type {import('tailwindcss').Config}*/
const config = {
    content: [
        './src/**/*.{html,js,svelte,ts}',
        './node_modules/flowbite/**/*.js'
    ],
    plugins: [
        require('flowbite/plugin')
    ],
    darkMode: 'class',
    /* https://tailwindcss.com/docs/theme */
    theme: {
        extend: {
        }
    },
};

module.exports = config;
