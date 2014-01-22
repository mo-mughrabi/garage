'use strict';

function MyVehicleController($scope, $http, Car) {

    $scope.next = null;
    $scope.cars = [];

    Car.query({my_vehicle: true},
        // success
        function(data) {
            $scope.next = data.next;
            $scope.cars = data.results;
        },
        // error
        function(data) {

        }
    );

    $scope.mark_sold = function(id, index) {
        Car.update({
            id      : id,
            status  : 'S'
        }, function(data) {
            $scope.cars[index].status_label = data.status_label;
            $scope.cars[index].status = data.status;
        });
    }

    $scope.prepareDelete = function(id, index) {
        $scope.delete_car_id = id;
        $scope.delete_car_index = index;
        $scope.delete_car_name = $scope.cars[index].model_display.make_display + ' ' +
                                 $scope.cars[index].model_display.model_display + ' ' +
                                 $scope.cars[index].model_display.trim_display;
    }

    $scope.delete = function() {
        Car.delete(
            {id: $scope.delete_car_id},
            // on success
            function() {
                // remove the element from cars array and it will be
                // automatically updated by ng-repeat
                $scope.cars.splice($scope.delete_car_index, 1);
            }
        );
    }

    $scope.loadMore = function() {
        if($scope.next) {
            $scope.$broadcast('loading_started');

            $http.get($scope.next)
            .success(function (data, status) {
                $scope.next = data.next;
                $scope.cars = $scope.cars.concat(angular.fromJson(data.results));
                $scope.$broadcast('loading_ended');
            })
            .error(function (data, status) {
                $scope.$broadcast('loading_ended');
            });
        }
    }


    $scope.$on('loading_started', function() {
        $scope.state = 'loading';
    });

    $scope.$on('loading_ended', function() {
        $scope.state = 'ready';
    });


}