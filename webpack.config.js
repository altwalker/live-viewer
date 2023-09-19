const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require('path')

let config = {
  target: 'web',
  entry: './src/app.js',
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'viewer/dist')
  },
  devServer: {
    static: './dist',
  },
  module: {
    rules: [
      { test: /\.html$/i, loader: 'html-loader' },
      { test: /\.css$/, use: [ MiniCssExtractPlugin.loader, 'css-loader' ] },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
      favicon: './src/favicon.ico',
      meta: {
        'description': { name: 'description', content: '...' },
        'keyword': { name: 'keywords', content: '...' },
        'og:title': { property: 'og:title', content: '...' },
        'og:description': { property: 'og:description', content: '...' },
        'og:type': { property: 'og:type', content: 'website' },
        'og:url': { property: 'og:url', content: '...' },
        'og:image': { property: 'og:image', content: '...' },
        'twitter:card': { name: 'twitter:card', content: 'summary_large_image' },
        'twitter:title': { name: 'twitter:title', content: '...' },
        'twitter:description': { name: 'twitter:description', content: '...' },
        'twitter:image': { name: 'twitter:image', content: '...' }
      }
    }),
    new MiniCssExtractPlugin(),
    // new CopyPlugin({
    //   patterns: [
    //     { from: "./src/*.png", to: "[name].[ext]" },
    //   ],
    // }),
  ],
}

module.exports = function(env, argv) {
  if (argv.mode === 'development') {
    config.devtool = 'inline-source-map';
  }

  return config;
}
