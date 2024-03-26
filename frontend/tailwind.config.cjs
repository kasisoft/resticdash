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
            borderRadius: {
                'none': '0',
                'sm': '0',
                DEFAULT: '0',
                'lg': '0',
                'full': '0',
            },
            colors: {
                'primary': {
                    '50': '#FFFDF7',
                    '100': '#FFF9ED',
                    '200': '#FCEED4',
                    '300': '#FCE1BB',
                    '400': '#FABF87',
                    '500': '#F89554',
                    '600': '#DE7F45',
                    '700': '#BA5F2F',
                    '800': '#94431E',
                    '900': '#702C11',
                    '950': '#471707'
                }
            }
        }
    },
};

module.exports = config;
