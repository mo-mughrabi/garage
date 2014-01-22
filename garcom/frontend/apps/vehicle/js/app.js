'use strict';

angular.module('garage', []);

angular.module('admin', ['modelLookupServices', 'postServices']);

angular.module('home', ['modelLookupServices', 'postServices', 'browseDirectives']).config(
    function($routeProvider) {
        $routeProvider.
            when('/browse/:make',              { action: 'browse' }).
            when('/browse/:make/:model',       { action: 'browse' }).
            when('/browse/:make/:model/:trim', { action: 'browse' });
    }
);

angular.module('vehicleProfile', ['profileServices', 'profileDirectives']);

angular.module('newVehicle', ['modelLookupServices', 'postServices', 'newVehicleDirectives']).config(
    function($routeProvider, $httpProvider) {
        $routeProvider.
            when('/:make',                    { action: 'modelLookup' }).
            when('/:make/:year',              { action: 'modelLookup' }).
            when('/:make/:year/:model',       { action: 'modelLookup' }).
            when('/:make/:year/:model/:trim', { action: 'modelLookup' }).
            otherwise({ action: 'default' });

        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    }
);