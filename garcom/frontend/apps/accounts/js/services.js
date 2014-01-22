'use strict';

angular.module('vehicleServices', ['ngResource']).
    factory('Car', function($resource) {
        return $resource('/vehicle/api/cars/:id', {},
            {
                query:   {method:'GET',     isArray:false},
                delete:  {method:'DELETE',  isArray:false},
                update:  {method:'PUT',     isArray:false}
            }
        );
    });