// includes
var gulp = require('gulp');
var concat = require('gulp-concat');
var cssmin = require('gulp-cssmin');
var uglify = require('gulp-uglify');

// add any local css sources here
var css_sources = ['static/css/local.min.css',
                  ];

// add any local javascript sources here
var js_sources = ['static/js/local.min.js',
                 ];

// minify css
gulp.task('minify_css', function() {
    return gulp.src('static/css/*.css')
        .pipe(concat('local.min.css'))
        .pipe(cssmin())
        .pipe(gulp.dest('static/css/'))
});

// build css
gulp.task('build_css', function() {
    return gulp.src(css_sources)
        .pipe(concat('all.min.css'))
        .pipe(gulp.dest('static/built/'))
});

// minify js
gulp.task('minify_js', function() {
    return gulp.src('static/js/*.js')
        .pipe(concat('local.js'))
        .pipe(uglify())
        .pipe(gulp.dest('static/js/'))
});

// build js
gulp.task('build_js', function() {
    return gulp.src(js_sources)
        .pipe(concat('all.min.js'))
        .pipe(gulp.dest('static/built'))
});

// default task
gulp.task('default', ['minify_css', 'build_css', 'minify_js', 'build_js']);
