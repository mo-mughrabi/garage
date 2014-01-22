'use strict';

angular.module('browseDirectives', []).
    directive('post', function() {
        return {
            restrict: 'C',      // class
            transclude: false,
            link: function postLink($scope, $element) {
                $element.each(function(index) {
                    $(this).css('cursor', 'pointer');

                    $(this).click(function() {
                        var url = $(this).children('.infobox').children('.title').children('a').attr('href');
                        window.location = url;
                    });

                    $(this).hover(function() {
                            $(this).css('background-color', '#f4f4f4');
                            $(this).css('-moz-border-radius', '3px');
                            $(this).css('border-radius', '3px');
                        },
                        function() {
                            $(this).css('background-color', 'transparent');
                        });
                });
            }
        }
    }).
    directive('bsButtonsRadio', ['$parse', function($parse) {
        'use strict';
        return {
            restrict: 'A',
            require: '?ngModel',
            compile: function compile(tElement, tAttrs, transclude) {

                tElement.attr('data-toggle', 'buttons-radio');

                // Delegate to children ngModel
                if(!tAttrs.ngModel) {
                    tElement.find('a, button').each(function(k, v) {
                        $(v).attr('bs-button', '');
                    });
                }

                return function postLink(scope, iElement, iAttrs, controller) {

                    // If we have a controller (i.e. ngModelController) then wire it up
                    if(controller) {

                        iElement
                            .find('[value]').button()
                            .filter('[value="' + scope.$eval(iAttrs.ngModel) + '"]')
                            .addClass('active');

                        iElement.on('click.button.data-api', function (ev) {
                            scope.$apply(function () {
                                controller.$setViewValue($(ev.target).closest('button').attr('value'));
                            });
                        });

                        // Watch model for changes
                        scope.$watch(iAttrs.ngModel, function(newValue, oldValue) {
                            if(newValue !== oldValue) {
                                var $btn = iElement.find('[value="' + scope.$eval(iAttrs.ngModel) + '"]');
                                if($btn.length) {
                                    $.fn.button.Constructor.prototype.toggle.call($btn.data('button'));
                                }
                            }
                        });

                    }

                };
            }
        };

    }]);