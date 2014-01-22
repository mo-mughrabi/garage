'use strict';

angular.module('modelLookupServices', ['ngResource']).
    factory('Make', function($resource) {
        return $resource('/vehicle/api/makes', {},
            {
                query: {method:'GET', isArray:true}
            }
        );
    }).
    factory('Model', function($resource) {
        return $resource('/vehicle/api/models/:make/:year', {},
            {
                query: {method:'GET', isArray:true}
            }
        );
    }).
    factory('Trim', function($resource) {
        return $resource('/vehicle/api/trims/:make/:model/:year', {},
            {
                query: {method:'GET', isArray:true}
            }
        );
    }).
    factory('Year', function($resource) {
        return $resource('/vehicle/api/years/:make/:model/:trim', {},
            {
                query: {method:'GET', isArray:false}
            }
        );
    }).
    factory('Color', function($resource) {
        return $resource('/vehicle/api/colors', {},
            {
                query: {method:'GET', isArray:true}
            }
        );
    }).
    factory('ModelInstance', function($resource) {
        return $resource('/vehicle/api/models/:make/:model/:year/:trim', {},
            {
                save:  {method:'POST'}
            }
        );
    });