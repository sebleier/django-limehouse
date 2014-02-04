(function(window, $) {
    $(document).on('click', 'a[data-targets]', function(e) {
        /*
            TODO::

                * Clean up this mess
                * Structure it better
                * Be more specific with TODO recommendations
        */
        e.preventDefault();
        var href = this.href;
        var targets = $(this).data('targets');
        targets = targets.split(';')
        targets = targets.map(function(t) { return t.split(":"); });

        var state = {};
        for(var i = 0; i < targets.length; i++) {
            state[targets[i][0]] = $(targets[i][0]).html();
        }

        // If current state is null, then fill with state using the current
        // target's html
        if (window.history.state === null) {
            window.history.replaceState(state, '');
        }


        var templates = {}
        var templatesRetrieved = 0;
        var templatesRendered = 0;
        var context = null;

        function updateDom() {
            // Once all the templates have rendered, push the state to the history
            // and update the DOM with the rendered HTML.
            if (templatesRendered === targets.length) {
                window.history.pushState(state, null, href);
                for(var target in state) {
                    $(target).html(state[target]);
                }
            }
        }

        function renderTemplate(target, template) {
            template.render(context, function(err, html) {
                if (err) {
                    console.log(err.message)
                }
                state[target] = html;
                templatesRendered += 1;
                updateDom();
            });
        }

        function renderTemplates() {
            if (templatesRetrieved === targets.length && context !== null) {
                for(var target in templates) {
                    renderTemplate(target, templates[target])
                }
            }
        }

        function getTemplate(target, template) {
            $.get('/jstemplates/'+targets[i][1], function(template) {
                templates[target] = new plate.Template(template);
                templatesRetrieved += 1;
                renderTemplates();
            });
        }

        // get all the javascript templates
        for(var i = 0; i < targets.length; i++) {
            getTemplate(targets[i][0], targets[i][1]);
        }

        $.ajax(this.href, {
            type: "GET",
            cache: true,
            dataType: "json",
            headers: {
                'X-Context-Only': true
            },
            success: function(data, textStatus, jqXHR) {
                context = data;
                renderTemplates();
            }
        });
    });
    window.addEventListener('popstate', function(e) {
        if (e.state !== null) {
            for(var selector in e.state) {
               $(selector).html(e.state[selector]);
            }
        }

    });

    window.plate.Template.Meta.registerPlugin('loader',
        function(templateName, ready) {
            $.get('/jstemplates/'+templatesName, function(html) {
                ready(null, new plate.Template(html));
            });
        }
    );

})(window, jQuery)
