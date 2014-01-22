'use strict';

function AdminCtrl($scope, Car) {

    Car.query(
        {status: 'P'},
        function(data) {
            $scope.cars = data.results;
        }
    );


}