import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, View
from annoying.functions import get_object_or_None

from .models import Image, ImageList

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_image(request):
    return get_object_or_None(Image, pk=request.REQUEST.get("image_id"))

def get_lists(image):
    """Returns lists for image object"""
    image_lists = image.lists.all()
    lists = ImageList.objects.order_by('title')
    return [{
        "title": lst.title,
        "id": lst.pk,
        "in": lst in image_lists
    } for lst in lists]


class AjaxableResponseMixin(object):

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def success(self, data):
        resp = { "success": True }
        resp.update(data)
        return self.render_to_json_response(resp)

    def error(self, message):
        return self.render_to_json_response({
            "success": False,
            "error": message
        })


class Home(ListView):
    template_name = "imglist/home.html"
    model = Image
    context_object_name = 'images'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)


class NewList(View, AjaxableResponseMixin):
    def post(self, request, *args, **kwargs):
        list_name = request.REQUEST.get("list_name", None)
        if not list_name:
            return self.error("Your list must have a name.")
        image_list, created = ImageList.objects.get_or_create(
            title=list_name,
            defaults={
                "creator_ip": get_client_ip(request)
            }
        )
        if not created:
            return self.error("You already have a list named {}.".format(list_name))
        image = get_image(request)
        if not image:
            return self.error("Image doesn't exist.")
        image.lists.add(image_list)
        return self.success({
            "lists" : get_lists(image)
        })


class GetLists(View, AjaxableResponseMixin):
    def post(self, request, *args, **kwargs):
        image = get_image(request)
        if not image:
            return self.error("Image doesn't exist.")
        return self.success({
            "lists" : get_lists(image)
        })

class AddToList(View, AjaxableResponseMixin):
    """
    Adds image to the list
    """
    def post(self, request, *args, **kwargs):
        image = get_image(request)
        if not image:
            return self.error("Image doesn't exist.")
        lst = get_object_or_None(ImageList, pk=request.REQUEST.get("list_id"))
        if not lst:
            return self.error("Image list doesn't exist.")
        image.lists.add(lst)
        return self.success({
            "lists" : get_lists(image)
        })

class RemoveFromList(View, AjaxableResponseMixin):
    """
    Removes image form the list
    """
    def post(self, request, *args, **kwargs):
        image = get_image(request)
        if not image:
            return self.error("Image doesn't exist.")
        lst = get_object_or_None(ImageList, pk=request.REQUEST.get("list_id"))
        if not lst:
            return self.error("Image list doesn't exist.")
        image.lists.remove(lst)
        return self.success({
            "lists" : get_lists(image)
        })
