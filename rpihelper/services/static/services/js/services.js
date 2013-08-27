(function(globalSettings, $, _, window, undefined) {
    var Application = window.Application,
        settings = globalSettings.Services;

    var ServicesView = Backbone.View.extend({
        initialize: function(options) {
            this.templateSelectorPrefix = '#js-tmpl-services-';
            this.serviceCommandsActive = this.templateSelectorPrefix + 'service-commands-active';
            this.serviceCommandsInactive = this.templateSelectorPrefix + 'service-commands-inactive';

        },
        events: {
            'click .js-services-call-command': 'callCommand'
        },

        getTemplateSelector: _.memoize(function(command) {
            if (command === 'stop') {
                return this.serviceCommandsInactive;
            } else if (_.include(['start', 'restart'], command)) {
                return this.serviceCommandsActive;
            }
        }),
        getTemplate: _.memoize(function(templateSelector) {
            return $(templateSelector).html();
        }),
        setServiceCommandsTemplate: function(service, command) {
            var serviceNode = this.$('.js-services-service-' + service),
                commandsNode = serviceNode.children('.js-services-service-commands').first(),
                templateSelector = this.getTemplateSelector(command),
                template = this.getTemplate(templateSelector);

            commandsNode.html(_.template(template, {
                service: service
            }));
        },

        callCommand: function(event) {
            var button = $(event.target),
                service = button.data('service'),
                command = button.data('command'),

                onSuccess = function() {
                    this.setServiceCommandsTemplate(service, command);
                },

                params = {
                    data: {
                        service: service,
                        command: command
                    },
                    action: settings.sendServiceCommandUrl,
                    success: _.bind(onSuccess, this)
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
