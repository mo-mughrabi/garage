'use strict';

angular.module('login', ['AccountsDirectives']);


angular.module('register', []);


angular.module('recovery', []);


angular.module('profile', ['AccountsDirectives']);


angular.module('my_vehicles', ['vehicleServices', 'AccountsDirectives']).config(
    function($httpProvider) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    }
);

