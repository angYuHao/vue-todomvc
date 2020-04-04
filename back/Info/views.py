from django.views.generic.base import RedirectView
from django.http import HttpResponse
from Info.models import Fruits
import json


# Create your views here.
class AddView(RedirectView):
    def get(self, request):
        name = request.GET.get("name", "")
        checkstate = False
        if name != "":
            Fruits.objects.create(name=name, checkstate=checkstate)
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class DelView(RedirectView):
    def get(self, request):
        id = request.GET.get("id", "")
        if id != "":
            Fruits.objects.filter(id=id).delete()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')


class UpdateView(RedirectView):
    def get(self, request):
        id = request.GET.get("id", "")
        name = request.GET.get("name", "")
        if id != "":
            Fruits.objects.filter(id=id).update(name=name)
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')


class SelectView(RedirectView):
    def get(self, request):
        all_fruits = Fruits.objects.all()
        list_fruits = []
        for fruit in all_fruits:
            fruit1 = dict()
            fruit1['id'] = fruit.id
            fruit1['name'] = fruit.name
            fruit1['checkstate'] = fruit.checkstate
            list_fruits.append(fruit1)
        return HttpResponse(json.dumps(list_fruits), content_type='application/json')


