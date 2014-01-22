'use strict';

angular.module('AccountsDirectives', []).directive('glow', function () {
        return {
            // A : Attribute
            // E : Element
            // C : as css class
            restrict: 'A',
            link: function (scope, element) {
                element.hover(function() {
                    $(this).find('img').addClass('glow-effect');
                }, function() {
                    $(this).find('img').removeClass('glow-effect');
                })
            }
        };
    });