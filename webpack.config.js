const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const WorkboxPlugin = require('workbox-webpack-plugin')
const path = require('path')

const title = 'AltWalker\'s Live Viewer: A real-time viewer for AltWalker test runs.'
const description = 'This application provides real-time visualization for your AltWalker test runs, allowing you to gain deeper insights into test execution, track progress, and identify potential issues with ease.'
const keywords = 'altwalker, model-based-testing, testing'
const url = 'https://altwalker.github.io/live-viewer/'
const image = 'https://raw.githubusercontent.com/altwalker/live-viewer/main/img/meta.png'

const config = {
  target: 'web',
  entry: './src/app.js',
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'viewer/dist')
  },
  devServer: {
    static: './dist'
  },
  module: {
    rules: [
      { test: /\.html$/i, loader: 'html-loader' },
      { test: /\.css$/, use: [ MiniCssExtractPlugin.loader, 'css-loader' ] }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
      favicon: './src/favicon.ico',
      meta: {
        'description': { name: 'description', content: description },
        'keyword': { name: 'keywords', content: keywords },
        'og:title': { property: 'og:title', content: title },
        'og:description': { property: 'og:description', content: description },
        'og:type': { property: 'og:type', content: 'website' },
        'og:url': { property: 'og:url', content: url },
        'og:image': { property: 'og:image', content: image },
        'twitter:card': { name: 'twitter:card', content: 'summary_large_image' },
        'twitter:title': { name: 'twitter:title', content: title },
        'twitter:description': { name: 'twitter:description', content: description },
        'twitter:image': { name: 'twitter:image', content: image }
      }
    }),
    new MiniCssExtractPlugin(),
    new WorkboxPlugin.GenerateSW({
      clientsClaim: true,
      skipWaiting: true
    })
  ]
}

module.exports = function (env, argv) {
  if (argv.mode === 'development') {
    config.devtool = 'inline-source-map'
  }

  return config
}
