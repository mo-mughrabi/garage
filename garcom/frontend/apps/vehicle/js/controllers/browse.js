'use strict';

function BrowseCtrl($scope, $routeParams, $q, $location, Make, Model, Trim, Year, Color, Price, Mileage, Filter, Sort) {
    // broadcast a message to Filter listeners
    $scope.applyFilter = function() {
        Filter.apply($scope);
    }

    // reset models
    var resetModels = function() { $scope.models = []; $scope.model = '' }
    var resetTrims  = function() { $scope.trims = [];  $scope.trim = '' }

    var loadModel = function() {
        var deferred = $q.defer();

        if($scope.make) {
            $scope.models = Model.query({make: $scope.make, exist: 'yes'},
                function() {
                    deferred.resolve();
                }, function() {
                    deferred.reject();
                });
        } else {
            resetModels();
            deferred.resolve();
        }

        return deferred.promise;
    }

    var loadTrim  = function() {
        var deferred = $q.defer();

        if($scope.model) {
            $scope.trims = Trim.query({make: $scope.make, model: $scope.model, exist: 'yes'},
                function() {
                    deferred.resolve();
                }, function() {
                    deferred.reject();
                });
        } else {
            resetTrims();
            deferred.resolve();
        }

        return deferred.promise;
    }

    var loadYear  = function() {
        var deferred = $q.defer();

        Year.query({make: $scope.make, model: $scope.model, trim: $scope.trim, exist: 'yes'},
            function(data) {
                $scope.years = data.years;
                deferred.resolve();
            }, function() {
                deferred.reject();
            }
        );

        return deferred.promise;
    }

    // respond to route changes
    // this is needed if you enter a hased URL directly into the browser
    $scope.$on("$routeChangeSuccess",
        function( $currentRoute, $previousRoute ){
            $scope.make  = $routeParams.make || '';
            $scope.model = $routeParams.model || '';
            $scope.trim  = $routeParams.trim || '';
        }
    );

    // listeners to dropdowns changes
    $scope.makeChange = function() {
        resetModels();
        resetTrims();

        $scope.modelsLoading = "loading";
        var modelPromise = loadModel();
        modelPromise.then(function() {
            $scope.modelsLoading = "";
            var yearPromise = loadYear();

            yearPromise.then(function() {
                if($scope.make) $location.path('/browse' + '/' + $scope.make);
                Filter.apply($scope);
            })
        })
    }

    $scope.modelChange = function() {
        resetTrims();

        $scope.trimsLoading = "loading";
        var trimPromise = loadTrim();
        trimPromise.then(function() {
            $scope.trimsLoading = "";
            var yearPromise = loadYear();

            yearPromise.then(function() {
                if($scope.model) $location.path('/browse' + '/' + $scope.make + '/' + $scope.model);
                Filter.apply($scope);
            })
        })
    }

    $scope.trimChange = function() {
        var yearPromise = loadYear();

        yearPromise.then(function() {
            if($scope.trim) $location.path('/browse' + '/' + $scope.make + '/' + $scope.model + '/' + $scope.trim);
            Filter.apply($scope);
        })
    }

    // initial settings
    $scope.makes = Make.query({exist: 'yes'}, function() {
        Filter.apply($scope);
    });
    loadYear();
    $scope.colors = Color.query();
    Price.get({}, function(data) {
        $scope.prices = {
            min: data.min,
            max: data.max
        }
        $scope.priceFrom = $scope.prices.min;
        $scope.priceTo   = $scope.prices.max;
    });
    Mileage.get({}, function(data) {
        $scope.mileage = {
            min: data.min,
            max: data.max
        }
        $scope.mileageFrom = $scope.mileage.min;
        $scope.mileageTo   = $scope.mileage.max;
    });
    $scope.sort = '-created_at';

    $scope.$on('sort', function() {
        $scope.sort = Sort.message.sort;
        $scope.applyFilter();
    });

}