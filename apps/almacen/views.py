from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView
from forms import *
from django.http import HttpResponse,HttpResponseRedirect
from Teletak.mixins import SuccessMessageMixin

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class Index(LoginRequiredMixin, View):

    template_name = 'almacen/index.html'
    def get(self, request):
        return render(request, self.template_name)

class Operaciones(LoginRequiredMixin,View):
    template_name='almacen/operaciones/index.html'
    def get(self,request):
        return render(request,self.template_name)

class Ingresos(LoginRequiredMixin,View,SuccessMessageMixin):
    template_name='almacen/ingresos/index.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        ingresos_form= IngresoForm(request.POST)
        detalleingreso_form = DetalleIngresoForm(request.POST)
        producto_form = ProductoForm(request.POST)
        guiaremision_form = GuiaRemisionForm(request.POST)
        if ingresos_form.is_valid() and detalleingreso_form.is_valid() and producto_form.is_valid() \
                and guiaremision_form.is_valid():

            nuevo_item = ingresos_form.save(commit=False)
            nuevo_item.guia_remision = guiaremision_form.save()
            nuevo_item1 = detalleingreso_form.save(commit=False)
            nuevo_item1.id_ingreso=nuevo_item.save()
            nuevo_item1.codigo_producto=producto_form.save()
            nuevo_item1.save()
            success_message = 'Los datos se actualizaron correctamente'

            return HttpResponseRedirect("/ingresos/")
        else:
            template_name = 'almacen/ingresos'
            usuario_form = UsuarioForm
            ingresos_form = IngresoForm
            detalleingreso_form = DetalleIngreso
            producto_form = ProductoForm
            guiaremision_form = GuiaRemisionForm
            proveedores_form = ProveedoresForm

            return render(request,template_name,locals())

class IngresoMultiple(LoginRequiredMixin,SuccessMessageMixin,View):
    template_name = 'almacen/ingresos/ingreso_multiple.html'
    model = Ingreso

    def get(self,request):
        ctx = {}
        ctx['ingresos_form']= IngresoForm()
        ctx['formset'] = DetalleIngresoFormSet()

        ctx['guiaremision_form'] = GuiaRemisionForm()


        return render(request,self.template_name,ctx)

    def post(self,request):
        ingresos_form= IngresoForm(request.POST)
        guiaremision_form = GuiaRemisionForm(request.POST)
        if ingresos_form.is_valid()  and guiaremision_form.is_valid():

            nuevo_item = ingresos_form.save(commit=False)
            nuevo_item.guia_remision = guiaremision_form.save()
            nuevo_item.save()
            formset = DetalleIngresoFormSet(request.POST,instance=nuevo_item)
            if formset.is_valid():
                formset.save()
                success_message = 'Los datos se actualizaron correctamente'
                return HttpResponseRedirect("/ingresos/")
            return render(request,self.template_name,locals())

        else:

            return render(request,self.template_name,locals())




class Reingresos(LoginRequiredMixin,View):
    template_name='almacen/reingresos/index.html'
    def get(self,request):
        return render(request,self.template_name)


#salidas - HACIENDO PRUEBAS ----

from Teletak.mixins import JSONMixin
from rest_framework import generics,viewsets
from .serializers import SalidaSerializer

class Salidas(View,LoginRequiredMixin,JSONMixin):
    def get(self,request):
        salidas = Salida.objects.all()
        salida_form = SalidaForm()
        return render(request,'almacen/salidas/index.html',{'salida_form':salida_form,'salidas':salidas})
    def post(self,request):
        form = SalidaForm(request.POST)
        if form.is_valid():
            salida = form.save(commit=False)
            salida.fecha = time.strftime('%Y-%m-%d')
            salida.save()
        else:
            pass
#api
class SalidasCollection(generics.ListCreateAPIView):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer

class SalidasDelete(generics.RetrieveDestroyAPIView):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer

class SalidasViewSet(viewsets.ModelViewSet):
    queryset = Salida.objects.all()
    serializer_class = SalidaSerializer