'use strict';

angular.module('newVehicleDirectives', []).
    directive('fileupload', function() {
        return {
            restrict: 'A',  // attribute
            transclude: false,
            link: function postLink($scope, $element) {
                // initialize
                $element.fileupload();

                // options
                $element.fileupload('option', {
                    url: '/vehicle/api/image.json',
                    maxNumberOfFiles: 5,
                    maxFileSize: 5000000,
                    acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
                    process: [
                        {
                            action: 'load',
                            fileTypes: /^image\/(gif|jpeg|png)$/,
                            maxFileSize: 20000000 // 20MB
                        },
                        {
                            action: 'resize',
                            maxWidth: 1440,
                            maxHeight: 900
                        },
                        {
                            action: 'save'
                        }
                    ]
                });


                $element.bind('fileuploadcompleted', function (e, data) {
                    $.each($.parseJSON(data.jqXHR.responseText), function(idx, val) {
                        $scope.images = $scope.images.concat(val.image_id);
                        $scope.$apply();
                    })

                    // select the first uploaded image by default as the primary image
                    $element.find('table tbody.files tr.template-download').first().find('td').trigger('click');
                });

                $element.find('table tbody.files').delegate('tr.template-download', 'click', function(event) {
                    // only change if any of the cells is clicked - excluding cells contents/objects
                    if($(event.target).is('td')) {
                        $scope.primaryimage = $(this).attr('data-imageid');
                        $scope.$apply();

                        $(this).siblings().andSelf().children('td.size').find('span.muted').remove();
                        $(this).children('td.size').prepend('<span class="muted"><small>Cover Image</small><br/></span>');
                    }
                });
            }
        }
    }).
    directive('autosave', function() {
        return {
            restrict: 'A',  // attribute
            transclude: false,
            link: function postLink($scope, $element) {
                $($element).find('input[type="text"], select, textarea').blur(function() {
                    // save only if modelid is retrieved
                    if($scope.modelkey) {
                        $scope.save('D');
                    }
                });
            }
        }
    });