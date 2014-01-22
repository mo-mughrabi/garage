'use strict';

function PostsCtrl($scope, Car, Filter, Sort) {
    var init = function() {
        $scope.filter = Filter.message || {page: 1};
        $scope.page_has_next = true;
        $scope.cars = [];
    };

    // initialize values
    init();
    $scope.postsLayout = "stacked";

    // listening on 'filter' events
    $scope.$on('filter', function() {
        init();
        $scope.loadMore();
    });

    $scope.loadMore = function() {
        if($scope.page_has_next) {
            $scope.$broadcast('loading_started');
            Car.query($scope.filter,
                // success
                function(data) {
                    $scope.page_has_next = data.next;
                    $scope.cars = $scope.cars.concat(angular.fromJson(data.results));
                    $scope.filter.page++;
                    $scope.$broadcast('loading_ended');
                },
                // error
                function() {
                    $scope.page_has_next = false;
                    $scope.$broadcast('loading_ended');
                }
            );
        }
    };

    $scope.$on('loading_started', function() {
        $scope.state = 'loading';
    });

    $scope.$on('loading_ended', function() {
        $scope.state = 'ready';
    });


    $scope.$watch('sort', function(newValue, oldValue) {
        if(oldValue !== newValue) {
            Sort.apply(newValue);
        }
    })
    $scope.sort = '-created_at';
}