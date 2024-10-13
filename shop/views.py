from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Product, Service, Profile
from .forms import ProductForm, ServiceForm, SearchForm, CustomUserCreationForm, ProfileEditForm, ContactForm, ClientEditForm
from shop_messages.models import Message, Notification
from django.contrib.auth.models import User, Group

def is_admin(user):
    return user.groups.filter(name='Administradora de tienda').exists() or user.is_superuser

class IndexView(View):
    def get(self, request):
        products = Product.objects.all()
        services = Service.objects.all()
        
        is_admin_user = is_admin(request.user)

        return render(request, 'index.html', {
            'products': products,
            'services': services,
            'messages': messages.get_messages(request),
            'is_admin': is_admin_user,
        })

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_admin'] = is_admin(user)
        return context
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        product = self.object
        context['image_url'] = product.image.url if product.image else None
        context['stock'] = product.stock
        return context

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        return context

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ProductEditView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form, 'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado con éxito.")
            return redirect('products')
        else:
            messages.error(request, "Error, formulario inválido.")
        
        return render(request, 'edit_product.html', {'form': form, 'product': product})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ProductDeleteView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        messages.success(request, "Producto eliminado con éxito.")
        return redirect('products')

class ProductSearchView(View):
    def get(self, request):
        form = SearchForm()
        results = []
        search_form = SearchForm(request.GET)

        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Product.objects.filter(name__icontains=query)

        is_admin_user = is_admin(request.user)

        context = {'form': form, 'results': results, 'is_admin': is_admin_user,}

        return render(request, 'search_products.html', context)

class ServiceListView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        service = self.object
        context['image_url'] = service.image.url if service.image else None
        return context

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'create_service.html'
    success_url = reverse_lazy('services')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        return context

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ServiceEditView(View):
    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(instance=service)
        return render(request, 'edit_service.html', {'form': form, 'service': service})

    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(request.POST, request.FILES, instance=service)
        print("Valor de price enviado:", request.POST.get('price'))
        
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado con éxito.")
            return redirect('services')
        else:
            messages.error(request, "Error, formulario inválido.")
            print(form.errors)
        
        return render(request, 'edit_service.html', {'form': form, 'service': service})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ServiceDeleteView(View):
    def post(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        messages.success(request, "Servicio eliminado con éxito.")
        return redirect('services')

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido {username}!")
                return redirect('index')
            else:
                messages.error(request, "Error, datos incorrectos.")
        else:
            messages.error(request, "Error, formulario incorrecto.")

        return render(request, 'login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            Profile.objects.create(
                user=user,
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number']
            )
            username = form.cleaned_data.get('username')
            messages.success(request, f"¡Cuenta creada para {username}!")

            return redirect('login')
        else:
            messages.error(request, "Error, formulario inválido.")
        
        return render(request, 'register.html', {'form': form})

class ProfileView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'profile.html', {
            'profile': profile,
            'is_admin': is_admin(request.user),
        })
        
class EditProfileView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileEditForm(instance=profile, user=request.user)
        return render(request, 'edit_profile.html', {
            'form': form,
            'profile': profile,
            'is_admin': is_admin(request.user),
        })

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)

        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, "Perfil actualizado con éxito.")
            return redirect('profile')
        else:
            messages.error(request, "Error, formulario inválido.")
        
        return render(request, 'edit_profile.html', {
            'form': form,
            'profile': profile,
            'is_admin': is_admin(request.user),
        })

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            admin_users = User.objects.filter(groups__name='Administradora de tienda')

            if request.user.is_authenticated:
                sender = request.user
                sender_name = None
            else:
                sender = None
                sender_name = form.cleaned_data['name'] + ' (Usuario no autenticado)'

            if admin_users.exists():
                for admin_user in admin_users:
                    message = Message(
                        sender=sender,
                        recipient=admin_user,
                        content=form.cleaned_data['message'],
                        sender_name=sender_name
                    )
                    message.save()
                    Notification.objects.create(user=admin_user, message=message)

                return render(request, 'contact.html', {
                    'form': form,
                    'message': 'Mensaje enviado con éxito',
                })
            else:
                return render(request, 'contact.html', {
                    'form': form,
                    'message': 'No hay administradores disponibles.',
                })

        return render(request, 'contact.html', {
            'form': form,
            'message': 'Error al enviar el mensaje. Verifica los datos.',
        })

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class PagesListView(View):
    def get(self, request):
        products = Product.objects.all()
        services = Service.objects.all()
        return render(request, 'pages.html', {
            'products': products,
            'services': services,
        })

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClientListView(ListView):
    model = Profile
    template_name = 'clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        admin_group = Group.objects.get(name='Administradora de tienda')
        return Profile.objects.filter(user__is_superuser=False).exclude(user__groups=admin_group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = is_admin(self.request.user)
        return context
    
@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClientCreateView(CreateView):
    model = Profile
    template_name = 'create_client.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.save()

        Profile.objects.create(
            user=user,
            address=form.cleaned_data['address'],
            phone_number=form.cleaned_data['phone_number'])
        
        messages.success(self.request, f"¡Cliente {user.username} creado con éxito!")
        return redirect('clients')

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario.")
        return super().form_invalid(form)

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClientEditView(View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = ClientEditForm(instance=profile, user=profile.user)
        return render(request, 'edit_client.html', {'form': form, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = ClientEditForm(request.POST, request.FILES, instance=profile, user=profile.user)

        if form.is_valid():
            profile.user.email = form.cleaned_data['email']
            profile.user.save()
            form.save()
            messages.success(request, "Cliente actualizado con éxito.")
            return redirect('clients')
        else:
            messages.error(request, "Error, formulario inválido.")

        return render(request, 'edit_client.html', {'form': form, 'profile': profile})

@method_decorator(user_passes_test(is_admin), name='dispatch')
class ClientDeleteView(View):
    def post(self, request, pk):
        client = get_object_or_404(Profile, pk=pk)
        client.delete()
        messages.success(request, "Cliente eliminado con éxito.")
        return redirect('clients')