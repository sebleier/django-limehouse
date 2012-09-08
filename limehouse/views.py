import json
from django.http import HttpResponse


class ContextOptionalMixin(object):

    def render_to_response(self, context):
        if 'HTTP_X_CONTEXT_ONLY' in self.request.META:
            serialized = self.serialize(context)
            return HttpResponse(json.dumps(serialized), mimetype="application/json")
        return super(ContextOptionalMixin, self).render_to_response(context)

    def serialize(self):
        raise NotImplementedError("This method must be defined to serialize the context appropriately.")