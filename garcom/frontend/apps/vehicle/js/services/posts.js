'use strict';

angular.module('postServices', ['ngResource']).
    factory('Car', function($resource) {
        return $resource('/vehicle/api/cars', {},
            {
                get:     {method:'GET',  isArray:false},
                query:   {method:'GET',  isArray:false},
                create:  {method:'POST', isArray:false},
                update:  {method:'PUT',  isArray:false}
            }
        );
    }).
    factory('Price', function($resource) {
        return $resource('/vehicle/api/price', {},
            {
                get:     {method:'GET',  isArray:false}
            }
        );
    }).
    factory('Mileage', function($resource) {
        return $resource('/vehicle/api/mileage', {},
            {
                get:     {method:'GET',  isArray:false}
            }
        );
    }).
    factory('Filter', function($rootScope) {
        var Filter = {};

        var message = '';
        Filter.broadcast = function(message) {
            this.message = message;
            $rootScope.$broadcast('filter');
        }

        Filter.apply = function($scope) {
            Filter.broadcast({
                page: 1,
                model__make:         $scope.make || '',
                model__model:        $scope.model || '',
                model__trim:         $scope.trim || '',
                model__year__gte:    $scope.yearFrom || '',
                model__year__lte:    $scope.yearTo || '',
                asking_price__gte:   $scope.priceFrom || '',
                asking_price__lte:   $scope.priceTo || '',
                mileage__gte:        $scope.mileageFrom || '',
                mileage__lte:        $scope.mileageTo || '',
                condition:           $scope.condition || '',
                color__id:           $scope.color || '',
                sort:                $scope.sort || ''
            });
        }

        return Filter;
    }).
    factory('Sort', function($rootScope) {
        var Sort = {};

        var message = '';
        Sort.broadcast = function(message) {
            this.message = message;
            $rootScope.$broadcast('sort');
        }

        Sort.apply = function(sort) {
            Sort.broadcast({
                sort: sort || ''
            });
        }

        return Sort;
    });