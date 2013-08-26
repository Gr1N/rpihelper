(function(globalSettings, $, _, window, undefined) {
    var Application = window.Application,
        settings = globalSettings.Services;

    var ServicesView = Backbone.View.extend({
        events: {
            'click .js-services-call-command': 'callCommand'
        },
        callCommand: function(event) {
            var button = $(event.target),
                params = {
                    data: {
                        service: button.data('service'),
                        command: button.data('command')
                    },
                    action: settings.sendServiceCommandUrl
                };

            Application.trigger('submit-form-ajax', {
                params: params
            });
        }
    });

    $(function() {
        var servicesView = new ServicesView({
            el: $('#js-services-content')
        });
    });
})(window.Settings || {}, jQuery, _, window);
