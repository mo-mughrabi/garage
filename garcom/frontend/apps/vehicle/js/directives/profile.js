'use strict';

angular.module('profileDirectives', []).
    directive('thumbnails', function() {
        return {
            restrict: 'C',
            transclude: false,
            controller: function ($scope, $element, $attrs, Image, $window) {
                $scope.images = Image.query({
                    car_id: $attrs.carId
                }, function() {
                    $scope.selectImage(0);
                });

                $scope.selectImage = function(index) {
                    $scope.displayImage = $scope.images[index].image;
                }
            }
        }
    });