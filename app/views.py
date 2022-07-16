from django.shortcuts import render, redirect
from .models import  Post , Interaccion, Perfil 
from .forms import RegistroUsuarioForm, PostForm , PerfilUpdate, UsuarioUpdate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistroUsuarioForm()

    context = {'form' : form}
    return render(request, 'app/registro.html', context)


@login_required
def home(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    context = {'posts':posts, 'form' : form }
    return render(request, 'app/home.html', context)




def eliminar(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('home')


def perfil(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all()
    context = {'user':user, 'posts':posts}
    return render(request, 'app/perfil.html', context)



@login_required
def editar(request):
    if request.method == 'POST':
        usuario_form = UsuarioUpdate(request.POST, instance=request.user)
        perfil_form = PerfilUpdate(request.POST, request.FILES, instance=request.user.perfil)

        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            return redirect('home')
    else:
        usuario_form = UsuarioUpdate(instance=request.user)
        perfil_form = PerfilUpdate()

    context = {'usuario_form' : usuario_form, 'perfil_form' : perfil_form}
    return render(request, 'app/editar.html', context)



@login_required
def seguir(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Interaccion(from_user=current_user, to_user=to_user_id)
    rel.save()
    return redirect('home')


@login_required
def dejarSeguir(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Interaccion.objects.get(from_user=current_user.id, to_user=to_user_id)
    rel.delete()
    return redirect('home')