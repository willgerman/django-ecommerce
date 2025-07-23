// import { purgeCSSPlugin } from '@fullhuman/postcss-purgecss';
const { purgeCSSPlugin } = require('@fullhuman/postcss-purgecss');

module.exports = {
    plugins: [
        purgeCSSPlugin({
            content: [
                './templates/*.html',
                './templates/**/*.html',
            ]
        })
    ]
};
