'use strict';

angular.module('profileServices', ['ngResource']).
    factory('Image', function($resource) {
        return $resource('/vehicle/api/image', {},
            {
                get:     {method:'GET',  isArray:false},
                query:   {method:'GET',  isArray:true}
            }
        );
    });