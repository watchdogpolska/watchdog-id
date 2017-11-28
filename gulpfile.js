////////////////////////////////
//Setup//
////////////////////////////////

// Plugins
var gulp = require('gulp'),
    pjson = require('./package.json'),
    gutil = require('gulp-util'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    cssnano = require('gulp-cssnano'),
    rename = require('gulp-rename'),
    del = require('del'),
    plumber = require('gulp-plumber'),
    pixrem = require('gulp-pixrem'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    exec = require('child_process').exec,
    runSequence = require('run-sequence'),
    browserSync = require('browser-sync').create(),
    reload = browserSync.reload,
    concat = require('gulp-concat'),
    debug = require('gulp-debug'),
    spawn = require('child_process').spawn;
// Relative paths function


var pathsConfig = function (appName) {
    this.app = "./" + (appName || pjson.name);
    this.python = pythonPath = process.env.VIRTUAL_ENV || process.env.PWD || "/usr/local/lib/python2.7/";
    return {
        app: this.app,
        templates: this.app + '/templates',
        assets: {
            js: this.app + '/assets/js',
            images: this.app + '/assets/images',
            sass: this.app + '/assets/sass',
            fonts: this.app + '/assets/fonts'
        },
        js: this.app + '/static/js',
        images: this.app + '/static/images',
        css: this.app + '/static/css',
        fonts: this.app + '/static/fonts',
        vendor_js: [
            'node_modules/qrious/dist/qrious.js',
            'node_modules/bootstrap/js/dist/*.js'
        ]
    }
};

var paths = pathsConfig();

////////////////////////////////
//Tasks//
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function () {
    return gulp.src(paths.assets.sass + '/*.scss')
        .pipe(sass({includePaths: ['node_modules']}))
        .pipe(plumber()) // Checks for errors
        .pipe(autoprefixer()) // Adds vendor prefixes
        .pipe(pixrem())  // add fallbacks for rem units
        .pipe(browserSync.stream())
        .pipe(gulp.dest(paths.css))
        .pipe(rename({suffix: '.min'}))
        .pipe(cssnano()) // Minifies the result
        .pipe(gulp.dest(paths.css))
        .pipe(browserSync.stream())
        .pipe(debug());
});

// Javascript minification
gulp.task('scripts', function () {
    gulp.src([paths.assets.js].concat(paths.vendor_js))
        .pipe(plumber()) // Checks for errors
        .pipe(uglify()) // Minifies the js
        .pipe(concat('project.js'))
        .pipe(gulp.dest(paths.js))
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(paths.js))
        .pipe(browserSync.stream());
});

// Image compression
gulp.task('imgCompression', function () {
    return gulp.src(paths.assets.images + '/*')
        .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
        .pipe(gulp.dest(paths.images))
});

// Browser sync server for live reload
gulp.task('browserSync', function () {
    browserSync.init({
        proxy: "localhost:8000"
    });
});

// Run django server
gulp.task('runServer', function() {
    spawn('python', ['manage.py', 'runserver'], { stdio: 'inherit' })
});

// Default task
gulp.task('default', function () {
    runSequence(['styles', 'scripts', 'imgCompression'],
                 'runServer',
                 'browserSync');
});

////////////////////////////////
//Watch//
////////////////////////////////

// Watch
gulp.task('watch', ['default'], function () {

    gulp.watch(paths.assets.sass + '/*.scss', ['styles']);
    gulp.watch(paths.assets.js + '/*.js', ['scripts']).on("change", reload);
    gulp.watch(paths.assets.images + '/*', ['imgCompression']);
    gulp.watch(paths.templates + '/**/*.html').on("change", reload);

});
