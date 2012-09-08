================
Django Limehouse
================

A Django app to enhance sites by using pushState and ajax.  Limehouse relies on
`plate`_, which is a Django template language implementation written in
Javascript by `Chris Dickinson`_.


Quick Start
===========

Add ``limehouse`` to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'limehouse',
        ...
    )

Setup your server to serve your templates as static files. For example, in
Nginx with a path to your javascript-safe templates being,
/path/to/project/templates/jstemplates -- use something like this
configuration::

    location /jstemplates/ {
        root path/to/project/templates/;
    }

include `jquery`_, plate.js, and limehouse.js in your template::

    <script src="{{ STATIC_URL }}js/jquery.js"></script>
    <script src="{{ STATIC_URL }}js/plate.js"></script>
    <script src="{{ STATIC_URL }}js/limehouse.js"></script>

Annotate your links with ``data-targets``.  The contents should be in the form::

    data-targets="<jquery selector>:<template path>;<jquery selector>:<template path>"

Selector-template pairs are delimited by a colon and multiple pairs are
delimited by a semicolon.

For views that you want Limehouse-enabled, include a mixin::

    from django.views.generic import View
    from limehouse.views import ContextOptionalMixin


    class SomeView(ContextOptionalMixin, View):
        ...

        def serialize(self, context):
            # serialize context into something JSON serializeable
            ...



The Problem
===========

Previously, it's been hard for django developers to fully embrace using
client-side javascript templates because of a few problems.

First, there isn't a well known django template language implementation that
has been able to run on javascript.  This has forced developers/designers to
use different template engines, e.g. mustache or handlebars.  This comes with
the consequence of having to duplicate your logic if you want to maintain the
ability to render templates on the server.  This can be avoided if you use a
ported-to-python version of a javascript template language, but that doesn't
help people who like and want to use the Django template language.  `plate`_
is such an implementation and has most features of the python version.

Second,(TODO: come up with more reasons)


The Solution
============

Django Limehouse provides a framework for updating a page to another url,
without doing a page refresh. However, if javascript is not enabled or the
browser doesn't support any of the html5 features required, it will degrade
gracefully.


How does it work?
=================

Let's start with a simple page with a list of links that point to various
blog posts::

    <ul id="nav">
        {% for entry in entries %}
        <li><a href="{% url blog_entry slug=entry.slug %}">{{ entry.title }}</a></li>
        {% endfor %}
    </ul>

    <section id="body">
        {% include "blog/entry_body.html" with entry=current_entry %}
    </section>

Nothing special here, so let's enable Limehouse to load new entry pages via ajax::

    <ul id="nav">
        {% for entry in entries %}
        <li><a data-targets="#body:/blog/entry_body.html" href="{% url blog_entry slug=entry.slug %}">
            {{ entry.title }}
        </a></li>
        {% endfor %}
    </ul>

    <section id="body">
        {% include "blog/entry_body.html" with entry=current_entry %}
    </section>

Here we have the anchor tag annotated with a ``data-targets`` attribute, which
provides a declarative way to specify what html targets will use what templates.
You list out jQuery compatible selectors, paired with template paths and
Limehouse will fetch those templates.  The ``href`` of the anchor tag is left
unchanged and will be used to retrieve the context required to render the
view.

When the user clicks on the link, Limehouse will intercept the click event and
fetch all the templates specified in the ``data-targets`` attribute.  It also
uses ajax to retrieve the context for that view using a special HTTP header.
Once the context and all the templates are retrieved, Limehouse takes all the
targets and constructs a state object that contains a mapping between the
jQuery selectors and their current html.  We replace the current history state
with our newly created object and then start to construct the new html.

We use `plate`_ to render the templates, using a serialized form of the
context used to render the view server-side.  When all the templates are
finished rendering, a new state object is created for the page about to be
constructed and inserted into the history using ``pushState``. Then, the new
page is constructed with the rendered templates that are inserted into their
specified targets.

The advantage of this approach is that the "blog/entry_body.html" template
is one file, that works both on the front end as well as the back end.


The Django side of things
=========================

Limehouse comes with a special class-based view mixin that allows for this
functionality to work seamlessly.  When the client requests the view from
the server, it sends an HTTP request header ``X-Context-Only``, which is
used in the mixin during its ``render_to_response`` method.  Instead of
creating and rendering the templates server-side, the context is instead
returned in a serialized format.  That format is controlled by a method
called ``serialize`` and is responsible for returning data in a json
serializeable format.

That's about it.


Server
======

Templates are served as static files from a webserver from a templates
directory. It can be the same directory as your regular templates or from
a separate directory that is designated as your javascript-safe templates.
This might help you to make sure you're not including any templates with tags
require being on the server.

One of the neat aspects of this approach is that a template can be cached by
the browser and prevent the entire template from transferring over the wire.
This means that once the templates have been cached, the only thing
transferring over the wire will be data!


Caveats
=======

This approach is good at moving between pages, but it may not be a good way to
preforming application logic or real-time state changes.  For example, you
probably can't use a link to delete a resource, because you are probably
going to be deleting nodes in the DOM. That can have deeper implications than
simply replacing the inner HTML of a node.  Similarly, it may not be a good
idea to be POSTing data to a view.

Plate's implementation is also incomplete, since it can only handle local data.
You can write template tags and filters that retrieve data from the server,
but the developer has to be aware that not all tags are going to work out of
the box.

Only works with class-based views right now, since it is easy to just to add
the mixin into any class-based views.







.. _plate: https://github.com/chrisdickinson/plate
.. _Chris Dickinson: http://neversaw.us/
.. jquery: http://code.jquery.com/jquery.min.js







