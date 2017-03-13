// -*- javascript -*-
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// webpack imports
var webpack = require('webpack')
var process = require('process')
var path = require('path')
var HtmlWebpackPlugin = require('html-webpack-plugin');

var devtool = ''

var rootDir = path.join(__dirname, '..')
var sourceDir = path.join(rootDir, 'react')
var configDir = path.join(rootDir, 'config')
var buildDir = path.join(rootDir, 'build')

// pugins
var plugins = []

// if we are building for production
if (process.env.NODE_ENV === 'production') {
    // use production plugins
    plugins.push(
        new HtmlWebpackPlugin({
            template: path.join(sourceDir, 'pyre.html'),
            inject: 'body',
            filename: path.join(buildDir, 'pyre.html')
        }),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),
        new webpack.optimize.UglifyJsPlugin(),
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.optimize.DedupePlugin()
    )
} else {
    // show me decent stack races
    devtool = "inline-source-map"
    // use devel plugins
    plugins.push(
        new HtmlWebpackPlugin({
            template: path.join(sourceDir, 'pyre.html'),
            inject: 'body',
            filename: path.join(buildDir, 'pyre.html')
        })
    )
}

// export webpack configuration object
module.exports = {
    entry: {
        pyre: path.join(sourceDir, 'pyre.js'),
    },
    output: {
        filename: path.join('[name].js'),
        path: buildDir,
    },
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                loader: 'babel',
                include: [ sourceDir, ],
                query: { extends: path.join(configDir, 'babelrc')}
            }, {
                test: /\.css$/,
                loaders: ['style', 'css'],
            }, {
                test: /\.(png|jpg|ttf|otf)$/,
                loader: 'url',
                query: {limit: 10*1024*1024},
            },
        ],
    },
    resolve: {
        extensions: ['', '.js', '.jsx'],
        root: [sourceDir],
    },

    plugins: plugins,
    devtool: devtool,
}

// end of file
