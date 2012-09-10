from limehouse.views import ContextOptionalMixin
from django.forms.models import model_to_dict
from django.views.generic import TemplateView

from models import Entry


class EntryDetailView(ContextOptionalMixin, TemplateView):
    template_name = 'blog/entry.html'

    def serialize(self, context):
        params = context['params']
        entry = Entry.objects.get(pk=params['pk'])
        data = {'entry': model_to_dict(entry)}
        data['created'] = entry.created.strftime("%B %d, %Y")
        return data

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        entry = Entry.objects.get(**kwargs)
        context['entry'] = entry

        # This is a hack until I can figure out better datetime handling
        context['created'] = entry.created.strftime("%B %d, %Y")
        return context

entry_detail = EntryDetailView.as_view()
