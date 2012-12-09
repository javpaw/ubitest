'use strict';

// Declare app level module which depends on filters, and services
angular.module('ubiApp',[]). //['ubiApp.filters', 'ubiApp.services', 'ubiApp.directives']).
  // config([
  // '$routeProvider', function($routeProvider) {
  //   $routeProvider.when('/view1', {template: 'partials/partial1.html', controller: MyCtrl1});
  //   $routeProvider.when('/view2', {template: 'partials/partial2.html', controller: MyCtrl2});
  //   $routeProvider.otherwise({redirectTo: '/view2'});
  // }
  // ]).
  config([
   '$interpolateProvider',function($interpolateProvider){
    $interpolateProvider.startSymbol('<{');
    $interpolateProvider.endSymbol('}>');
  }
  ]);
