import json
from django.http import HttpResponse
from django.views.generic import ListView, View

from .models import Image, ImageList

class AjaxableResponseMixin(object):

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


class Home(ListView):
    template_name = "imglist/home.html"
    model = Image
    context_object_name = 'images'


class AddList(View, AjaxableResponseMixin):
    def post(self, request, *args, **kwargs):
        image_id = request.REQUEST.get("image_id", 0)
        list_name = request.REQUEST.get("list_name", None)
        if not list_name:
            return self.render_to_json_response({
                "success": False,
                "error": "Your list must have a name."
            })
        image_list, created = ImageList.objects.get_or_create(
            title=list_name,
            defaults={
                "creator_ip": self.get_client_ip(request)
            }
        )
        if not created:
            return self.render_to_json_response({
                "success": False,
                "error": "You already have a list named {}.".format(list_name)
            })
        image = Image.objects.get(pk=image_id)
        image.lists.add(image_list)
        return self.render_to_json_response({
            "success": True,
        })

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
