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
                this.setTemplate(this.systemInfoTemplateSelector, this.prepareData(response.data));

                _.delay(_.bind(this.getSystemInfo, this), 2000);
            }, this);

            Application.trigger('submit-form-ajax', {
                params: {
                    action: settings.systemInfoUrl,
                    success: onSuccess
                }
            });
        },
        prepareData: function(data) {
            var prepareMemory = function(memory) {
                    var gbb = Math.pow(1024, 3);
                    _.each(['total', 'used'], function(type) {
                        var bytes = memory[type];
                        memory[type] = bytes < gbb ? toMb(bytes) : toGb(bytes);
                    });
                },
                toMb = function(bytes) {
                    return Math.floor(bytes / Math.pow(1024, 2)) + 'Mb';
                },
                toGb = function(bytes) {
                    return Math.floor(bytes / Math.pow(1024, 3)) + 'Gb';
                };

            data.boot_time = new Date(data.boot_time * 1000).toLocaleString();

            prepareMemory(data.virtual_memory);
            prepareMemory(data.swap_memory);

            _.each(data.disks, function(disk) {
                prepareMemory(disk);
            });

            _.each(data.processes[0], function(process) {
                var mp = process.memory_percent,
                    ct = process.cpu_times;

                process.memory_percent = mp ? mp.toString().slice(0, 4) : null;
                process.cpu_times_system = ct ? ct.system.toString().slice(0, 4) : null;
            });

            return data;
        }
    });

    $(function() {
        var systemMonitorView = new SystemMonitorView({
            el: $('#js-sysmonitor-content')
        });
    });
})(window.Settings || {}, jQuery, _, window);
