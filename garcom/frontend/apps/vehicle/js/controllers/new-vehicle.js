'use strict';

function NewVehicleCtrl($scope, $routeParams, $q, $window, Car, Make, Model, Trim, Year, ModelInstance, Color) {
    // init
    $scope.makes = Make.query();
    $scope.images = [];
    $scope.colors = Color.query();

    // reset models
    var resetYears = function() { $scope.years = [];   $scope.year = '' }
    var resetModels = function() { $scope.models = []; $scope.model = '' }
    var resetTrims  = function() { $scope.trims = [];  $scope.trim = '' }

    $scope.loadYear  = function() {
        var deferred = $q.defer();

        if($scope.make) {
            Year.query({make: $scope.make, model: $scope.model, trim: $scope.trim},
            function(data) {
                $scope.years = data.years;
                deferred.resolve();
            }, function() {
                    deferred.reject();
            });
        }

        return deferred.promise;
    }

    $scope.loadModel = function() {
        var deferred = $q.defer();

        $scope.models = ($scope.year) ? Model.query(
            {
                make: $scope.make,
                year: $scope.year
            }, function() {
                deferred.resolve();
            }, function() {
                deferred.reject();
            }) : [];

        return deferred.promise;
    }

    $scope.loadTrim  = function() {
        var deferred = $q.defer();

        $scope.trims  = ($scope.model) ? Trim.query(
            {
                make: $scope.make,
                model: $scope.model,
                year: $scope.year
            }, function() {
                deferred.resolve();
            }, function() {
                deferred.reject();
            }) : [];

        return deferred.promise;
    }

    $scope.loadKey   = function() {
        if($scope.make && $scope.year && $scope.model) {
            ModelInstance.get({
                make:  $scope.make,
                model: $scope.model,
                year:  $scope.year,
                trim:  $scope.trim
            }, function(data) {
                $scope.modelkey = data.model__id;
            }, function() {
                $scope.modelkey = '';
            });
        }
    };

    // listener on route changes
    $scope.$on("$routeChangeSuccess",
        function( $currentRoute, $previousRoute ){
            $scope.make  = $routeParams.make  || $scope.make;
            $scope.year  = $routeParams.year  || $scope.year;
            $scope.model = $routeParams.model || $scope.model;
            $scope.trim  = $routeParams.trim  || $scope.trim;
        }
    );

    // propogate resets for sets
    // i.e. if makes is changed, years is set to empty which will
    // trigger $watch('years') and set models to empty, and so on
    $scope.$watch('makes',  function() { resetYears(); })
    $scope.$watch('years',  function() { resetModels(); })
    $scope.$watch('models', function() { resetTrims();  })

    // propogate reset for single elements
    $scope.$watch('make',   function() {
        resetYears();
        resetModels();
        resetTrims();

        $scope.yearsLoading = "loading";
        var promise = $scope.loadYear();

        promise.then(function() {
            $scope.yearsLoading = "";
        })
    })
    $scope.$watch('year',   function() {
        resetModels();
        resetTrims();

        $scope.modelsLoading = "loading";
        var promise = $scope.loadModel();

        promise.then(function() {
            $scope.modelsLoading = "";
        })
    })
    $scope.$watch('model',  function() {
        resetTrims();

        $scope.trimsLoading = "loading";
        var promise = $scope.loadTrim();
        promise.then(function() {
            $scope.trimsLoading = "";
            if($scope.trims.length == 0) $scope.loadKey()
        })
    })
    $scope.$watch('trim', function() {
        $scope.loadKey();
    })


    // form submission/draft
    $scope.save = function(status) {
        var params = {
            model_4:        $scope.modelkey,
            description:    $scope.description,
            mileage:        $scope.mileage,
            asking_price:   $scope.price,
            color:          $scope.color,
            condition:      $scope.condition,
            images:         $scope.images,
            primary_image:  $scope.primaryimage,
            contact_email:  $scope.email,
            contact_phone:  $scope.phone,
            status:         status || 'P'
        }

        var deferred = $q.defer();
        if($scope.carID) {
            params.id = $scope.carID;
            Car.update(params,
                function(data) {
                    $scope.response = data;
                    deferred.resolve();
                },
                function(data) {
                    $scope.response = data;
                    deferred.reject();
                }
            );
        } else {
            Car.create(params,
                function(data) {
                    $scope.response = data;
                    deferred.resolve();
                },
                function(data) {
                    $scope.response = data;
                    deferred.reject();
                }
            );
        }

        deferred.promise.then(function() {
            $scope.carID = $scope.response.id;

            if($scope.response.redirect) {
                $window.location.href = $scope.response.redirect;
            }
        }, function() {
            if(status != 'D') {
                $scope.errors = $scope.response.data.errors;
            }
        });
    }
}


function ModelSuggestionCtrl($scope, $q, $window, ModelInstance) {
    $scope.data = {}

    $scope.save = function() {
        var deferred = $q.defer();
        ModelInstance.save($scope.data,
            function(data) {
                $scope.response = data;
                deferred.resolve();
            },
            function(data) {
                $scope.response = data;
                deferred.reject();
            }
        );

        deferred.promise.then(function() {
            if($scope.response.redirect) {
                $window.location.href = $scope.response.redirect;
            }
        }, function() {
            // error
        });
    }
}