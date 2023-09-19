const HtmlWebpackPlugin = require('html-webpack-plugin')
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
      { test: /\.css$/, use: [ 'style-loader', 'css-loader' ] },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({ template: './src/index.html', favicon: './src/favicon.ico' })
  ],
}

module.exports = function(env, argv) {
  if (argv.mode === 'development') {
    config.devtool = 'inline-source-map';
  }

  return config;
}
