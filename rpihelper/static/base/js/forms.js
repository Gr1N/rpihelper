(function(settings, $, _, window, undefined) {
    var Application = window.Application,

        AjaxForms = {
            submit: function(selector, params) {
                var form = $(selector),
                    defaultParams = {

                    };
                params = _.defaults(params || {}, defaultParams);

                var processingMaximumTime = 10,
                    processingStartTime,
                    processing = false;

                var onRequestSuccess = function(response, status, request) {
                        console.log('AjaxForms:onRequestSuccess:response', response);
                        processing = false;

                        if (_.isUndefined(response)) {
                            console.log('AjaxForms:onRequestSuccess:NotImplementedError!');
                        }

                        if (response.status === 'ok') {
                            if (params.success) {
                                params.success.call(this, response);
                            }

                            return;
                        }

                        if (response.status === 'processing') {
                            var date = new Date();
                            if (_.isUndefined(processingStartTime)) {
                                processingStartTime = date.getTime();
                            }

                            var stillProcessing = date.getTime() - processingStartTime < processingMaximumTime * 1000;
                            if (stillProcessing) {
                                processing = true;
                                _.delay(checkProcessingStatus, 1000, response.status_url, this);
                                return;
                            }

                            console.log('AjaxForms:onRequestSuccess:processing:error');
                            return;
                        }

                        if (response.status === 'error') {
                            if (params.error) {
                                params.error.call(this, response);
                            }
                        }
                    },
                    onRequestError = function(request, text, errorThrown) {
                        console.log('AjaxForms:onRequestError:NotImplementedError!');
                    },
                    onRequestComplete = function() {
                        console.log('AjaxForms:onRequestComplete:NotImplementedError!');
                    },
                    checkProcessingStatus = function(statusUrl, context) {
                        $.ajax({
                            type: 'get',
                            url:  statusUrl,
                            dataType: 'json',
                            context: context,
                            success: onRequestSuccess,
                            error: onRequestError,
                            complete: onRequestComplete,
                            cache: false
                        });
                    },

                    submitAjax = function() {
                        $.ajax({
                            type: form.attr('method') || 'post',
                            url:  params.action || form.attr('action'),
                            data: params.data || form.serializeArray(),
                            dataType: 'json',
                            context: params.context,
                            success: onRequestSuccess,
                            error: onRequestError,
                            complete: onRequestComplete
                        });
                    };

                submitAjax();
                return true;
            }
        };

    Application.on('submit-form-ajax', function(options) {
        AjaxForms.submit(options.selector, options.params);
    });
})(window.Settings || {}, jQuery, _, window);
