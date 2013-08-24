(function(globalSettings, $, _, window, undefined) {
    var Application = window.Application,
        settings = globalSettings.SysMonitor;

    var SystemMonitorView = Backbone.View.extend({
        initialize: function(options) {
            this.templateSelectorPrefix = '#js-tmpl-sysmonitor-';
            this.systemInfoTemplateSelector = this.templateSelectorPrefix + 'system-info';

            this.getSystemInfo();
        },

        getTemplate: _.memoize(function(templateSelector) {
            return $(templateSelector).html();
        }),
        setTemplate: function(templateSelector, data) {
            var template = this.getTemplate(templateSelector);
            this.$el.html(_.template(template, data));
        },
        getSystemInfo: function() {
            var onSuccess = _.bind(function(response) {
                this.setTemplate(this.systemInfoTemplateSelector, response.data);
            }, this);

            Application.trigger('submit-form-ajax', {
                params: {
                    action: settings.systemInfoUrl,
                    success: onSuccess
                }
            });

            _.delay(_.bind(this.getSystemInfo, this), 2000);
        }
    });

    $(function() {
        var systemMonitorView = new SystemMonitorView({
            el: $('#js-sysmonitor-content')
        });
    });
})(window.Settings || {}, jQuery, _, window);
