var path = require('path')
var webpack = require('webpack')
var BrowserSyncPlugin = require('browser-sync-webpack-plugin')
var BundleTracker = require('webpack-bundle-tracker');

var IS_PRODUCTION = process.env.NODE_ENV === 'production'

var ENTRY_POINTS = [
  './assets/app/index.js'
]

var JS_LOADERS = [
  'babel?cacheDirectory&presets[]=react,presets[]=es2015,presets[]=stage-0'
]

var PLUGINS = []
if (IS_PRODUCTION && process.env.MKT_ENV !== 'dev') {
  // Uglify in production, but not -dev.
  PLUGINS.push(
    new webpack.optimize.UglifyJsPlugin({
      mangle: {
          except: ['$super', '$', 'exports', 'require']
      }
    })
  )
  PLUGINS.push(
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"production"'
    })
  )
} else {
  PLUGINS.push(
    new BrowserSyncPlugin({
      host: '0.0.0.0',
      port: '4200',
      server: {
        baseDir: ['public', 'build'],
      }
    })
  )
  PLUGINS.push(
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"development"'
    })
  )
  PLUGINS.push(
      new BundleTracker({
	  filename: './webpack-stats.json'
      })
  )
}

module.exports = {
  entry: ENTRY_POINTS,
  output: {
    // Bundle will be served at /bundle.js locally.
    filename: 'bundle.js',
    // Bundle will be built at ./assets/bundle.
    path: './assets/bundle',
    publicPath: '/static/bundle/',
  },
 
  module: {
    loaders: [
      {
        // JS.
        exclude: /(node_modules|bower_components|vr-markup)/,
        loaders: JS_LOADERS,
        test: /\.js$/,
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader'
      },
	{
	        test: /\.scss$/,
	        loaders: ["style", "css", "sass"]
	    },
	,
	{
	        test: /\.(jpg|png|svg)$/,
	        loaders: [
		    'file-loader?name=[path][name].[ext]'
		        ]
	    },
      {
        test: /\.json$/,
        loader: 'json-loader'
      }
    ],
  },
  plugins: PLUGINS,
  resolve: {
    extensions: ['', '.js', '.json'],
    fallback: path.join(__dirname, 'node_modules'),
    modulesDirectories: [
      'src',
      'node_modules',
    ]
  },
  resolveLoader: {
    fallback: [path.join(__dirname, 'node_modules')]
  }
}
