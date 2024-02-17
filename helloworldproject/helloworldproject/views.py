from django.http import HttpResponse
from django.views.generic import TemplateView

def helloworldfunction(request):
    return HttpResponse('<h1>HelloWorld!</h1>')

class helloworldClass(TemplateView):
    template_name = 'hello.html'