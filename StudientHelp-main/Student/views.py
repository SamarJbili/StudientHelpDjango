from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic import View ,ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post,Stage, Logement , Transport
from django.db.models import Q
from .models import Stage, Logement, ÉvenClub, ÉvenSocial, Transport, Recommandation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Comment, Like
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Stage, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Count
from .models import Stage, Logement, ÉvenClub, ÉvenSocial, Transport, Recommandation
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Notification

from .models import Notification

from .models import Comment, Notification
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


class acceuilView(ListView):
    template_name = 'acceuil.html'
    context_object_name = 'posts'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_likes'] = [like.post.id for like in user.user_likes.all()] if user.is_authenticated else []
        return context
   
def inscription(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès!')
            return redirect('acceuil')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/inscription.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour la session de l'utilisateur pour éviter la déconnexion
            messages.success(request, 'Votre mot de passe a été changé avec succès!')
            return redirect('acceuil')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})


class EvenementCulturelCreateView(LoginRequiredMixin,CreateView):
    model = ÉvenClub
    template_name = 'forms/evenementCult_form.html'
    success_url = reverse_lazy('eventCult-list')  # Mettez à jour avec votre URL de succès

    fields = ['Title','Type', 'Image', 'Description','Intitulé','Lieu','ContactInfo','Club']
    def form_valid(self, form):
        # Récupérer l'instance de post créée
        post = Post.objects.create(
            Title=form.cleaned_data['Title'],
            Type=form.cleaned_data['Type'],
            Image=form.cleaned_data['Image'],
            author=self.request.user,
            Catg="even_club"

        )
         # Enregistrer l'ID du post dans le formulaire Logement
        even_club = form.save(commit=False)
        even_club.author = self.request.user
        even_club.post_id = post.id  # Assigne l'ID du post à l'attribut post_id de Logement
        even_club.save()
        return super().form_valid(form)
    

class EvenementScientifiqueCreateView(LoginRequiredMixin,CreateView):
    model = ÉvenSocial
    template_name = 'forms/evenementSc_form.html'
    fields = ['Title', 'Type',  'Image','Description','Intitulé','Lieu','ContactInfo','Prix']
    success_url = reverse_lazy('eventSc-list')  # Mettez à jour avec votre URL de succès
    def form_valid(self, form):
        # Récupérer l'instance de post créée
        post = Post.objects.create(
            Title=form.cleaned_data['Title'],
            Type=form.cleaned_data['Type'],
            Image=form.cleaned_data['Image'],
            author=self.request.user,
            Catg="even_social"

        )
         # Enregistrer l'ID du post dans le formulaire Logement
        even_social = form.save(commit=False)
        even_social.author = self.request.user
        even_social.post_id = post.id  # Assigne l'ID du post à l'attribut post_id de Logement
        even_social.save()
        return super().form_valid(form)

class TransportCreateView(LoginRequiredMixin,CreateView):
    model = Transport
    template_name = 'forms/transport_form.html'
    fields = ['Title',  'Type', 'Image', 'Départ', 'Destination', 'Heure_dep', 'Nbre_sièges', 'Contactinfo']
    success_url = reverse_lazy('transport-list') # Mettez à jour avec votre URL de succès
    def form_valid(self, form):
        # Récupérer l'instance de post créée
        post = Post.objects.create(
            Title=form.cleaned_data['Title'],
            Type=form.cleaned_data['Type'],
            Image=form.cleaned_data['Image'],
            author=self.request.user,
            Catg="transport"

        )
        # Enregistrer l'ID du post dans le formulaire Logement
        transport = form.save(commit=False)
        transport.author = self.request.user
        transport.post_id = post.id  # Assigne l'ID du post à l'attribut post_id de Logement
        transport.save()
        return super().form_valid(form)

class StageCreateView(LoginRequiredMixin, CreateView):
    model=Stage
    template_name = 'forms/stageform.html' # Assurez-vous que votre modèle a un formulaire associé à ce modèle
    fields = ['Title', 'Type', 'Image', 'Stage_type', 'Société', 'Durée', 'Sujet', 'Contactinfo', 'Spécialité']
    success_url = reverse_lazy('stage-list')  # Mettez à jour avec votre URL de succès
    def form_valid(self, form):
        # Récupérer l'instance de post créée
        post = Post.objects.create(
            Title=form.cleaned_data['Title'],
            Type=form.cleaned_data['Type'],
            Image=form.cleaned_data['Image'],
            author=self.request.user,
            Catg="stage"

        )
        # Enregistrer l'ID du post dans le formulaire Logement
        stage = form.save(commit=False)
        stage.author = self.request.user
        stage.post_id = post.id  # Assigne l'ID du post à l'attribut post_id de Logement
        stage.save()
        return super().form_valid(form)


class LogementCreateView(LoginRequiredMixin, CreateView):
    model = Logement
    template_name = 'forms/logement_form.html'
    success_url = reverse_lazy('logement-list')  # Mettez à jour avec votre URL de succès
    fields = ['Title', 'Type', 'Image', 'Localisation', 'Description', 'Contactinfo']

    def form_valid(self, form):
        # Récupérer l'instance de post créée
        post = Post.objects.create(
            Title=form.cleaned_data['Title'],
            Type=form.cleaned_data['Type'],
            Image=form.cleaned_data['Image'],
            author=self.request.user,
            Catg="logement"
        )
        # Enregistrer l'ID du post dans le formulaire Logement
        logement = form.save(commit=False)
        logement.author = self.request.user
        logement.post_id = post.id  # Assigne l'ID du post à l'attribut post_id de Logement
        logement.save()
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'List/Postdetail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        print(f"Post category: {post.Catg}")  # Debugging line

        if (post.Catg == 'logement'):
            logement = get_object_or_404(Logement, id=post.id)
            context['logement'] = logement
            
        elif post.Catg == 'stage':
            stage = get_object_or_404(Stage, id=post.id)
            context['stage'] = stage
            
        elif post.Catg == 'even_club':
            even_club = get_object_or_404(ÉvenClub, id=post.id)
            context['even_club'] = even_club
            
        elif post.Catg == 'even_social':
            even_social = get_object_or_404(ÉvenSocial, id=post.id)
            context['even_social'] = even_social
            
        elif post.Catg == 'transport':
            transport = get_object_or_404(Transport, id=post.id)
            context['transport'] = transport
            
        elif post.Catg == 'recommandation':
            recommandation = get_object_or_404(Recommandation, id=post.id)
            context['recommandation'] = recommandation

        return context
def about (request):

    return render(request, 'about.html')

class LogementListView(ListView):
    model = Post
    template_name = 'List/logementList.html'

    def get_queryset(self):
        # Filtrer les objets pour n'inclure que ceux avec la catégorie "logement"
        queryset = super().get_queryset()
        return queryset.filter(Catg="logement")

   
class StageListView(ListView):
    model = Post
    template_name = 'List/liststage.html' 

    def get_queryset(self):
        # Filtrer les objets pour n'inclure que ceux avec la catégorie "logement"
        queryset = super().get_queryset()
        return queryset.filter(Catg="stage")

 
class TransportListView(ListView):
    model = Post
    template_name = 'List/TransportList.html' 
    def get_queryset(self):
        # Filtrer les objets pour n'inclure que ceux avec la catégorie "logement"
        queryset = super().get_queryset()
        return queryset.filter(Catg="transport")
     
class eventCultView(ListView):
    model = Post
    template_name = 'List/EvenementCulturelList.html' 
    def get_queryset(self):
        # Filtrer les objets pour n'inclure que ceux avec la catégorie "logement"
        queryset = super().get_queryset()
        return queryset.filter(Catg="even_club")

class eventScView(ListView):
    model = Post
    template_name = 'List/EvenementScientifiqueList.html' 
    def get_queryset(self):
        # Filtrer les objets pour n'inclure que ceux avec la catégorie "logement"
        queryset = super().get_queryset()
        return queryset.filter(Catg="even_social")
    



class EvenementCulturelUpdateView(LoginRequiredMixin,UpdateView):
    model = ÉvenClub
    template_name = 'List/update/updatelogement.html'
    fields = ['Title','Type', 'Image', 'Description','Intitulé','Lieu','ContactInfo','Club']
    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    success_url = reverse_lazy('mespost-view')  # Mettez à jour avec votre URL de succès

class EvenementScientifiqueUpdateView(LoginRequiredMixin,UpdateView):
    model = ÉvenSocial
    template_name = 'List/update/updatelogement.html'
    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    fields = ['Title', 'Type',  'Image','Description','Intitulé','Lieu','ContactInfo','Prix']
    success_url = reverse_lazy('mespost-view')  # Mettez à jour avec votre URL de succès

class TransportUpdateView(LoginRequiredMixin,UpdateView):
    model = Transport
    template_name = 'forms/transport_form.html'
    success_url = reverse_lazy('mespost-view') # Mettez à jour avec votre URL de succès
    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    fields = ['Title',  'Type', 'Image', 'Départ', 'Destination', 'Heure_dep', 'Nbre_sièges', 'Contactinfo']

class StageUpdateView(LoginRequiredMixin,UpdateView):
    model = Stage
    template_name = 'forms/stage_from.html'
    fields = ['Title', 'Type', 'Image', 'Stage_type', 'Société', 'Durée', 'Sujet', 'Contactinfo', 'Spécialité']
    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    success_url = reverse_lazy('mespost-view')# Mettez à jour avec votre URL de succès

class LogementUpdateView(LoginRequiredMixin,UpdateView):
    model = Logement
    template_name ='List/update/updatelogement.html'
    success_url = reverse_lazy('mespost-view')# Mettez à jour avec votre URL de succès
    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    fields = ['Title','Type', 'Image', 'Localisation', 'Description', 'Contactinfo']







class DeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('mespost-view')
    template_name = 'List/confirmdeleteeventSc.html'




def inputform (request):
    return render(request,'List/inputform.html')


class MesPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(author=user)

        # Debugging: print posts to the console
        print(posts)

        context = {
            'posts': posts,
        }

        return render(request, 'List/mespost.html', context)


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Search in all relevant models using Django's Q operator
        results += Logement.objects.filter(Q(Title__icontains=query))
        results += Stage.objects.filter(Q(Title__icontains=query))
        results += ÉvenClub.objects.filter(Q(Title__icontains=query))
        results += ÉvenSocial.objects.filter(Q(Title__icontains=query))
        results += Transport.objects.filter(Q(Title__icontains=query))

  
    context = {
        'results': results,
        'query': query,
    }

    return render(request, 'List/search_results.html', context)







def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès!')
            return redirect('acceuil')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/inscription.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Met à jour la sessio
            messages.success(request, 'Votre mot de passe a été changé avec succès!')
            return redirect('acceuil')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})



class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'add_comment.html'

    def form_valid(self, form):
        # Obtenir l'objet Post associé à partir de l'URL
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Ajouter l'auteur et l'objet de contenu au formulaire de commentaire
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})
    
@login_required
def like(request, post_id):
        author = request.user
        post = get_object_or_404(Post, id=post_id)
        liked = Like.objects.filter(author=author, post=post).count()

        if not liked:
            Like.objects.create(author=author, post=post)
            post.likes += 1
        else:
            Like.objects.filter(author=author, post=post).delete()
            post.likes -= 1

        post.save()
        return HttpResponseRedirect(reverse('acceuil'))

class PostDetailView(DetailView):
    model = Post
    template_name = 'List/Postdetail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        print(f"Post category: {post.Catg}")  # Debugging line

        if (post.Catg == 'logement'):
            logement = get_object_or_404(Logement, id=post.id)
            context['logement'] = logement
            
        elif post.Catg == 'stage':
            stage = get_object_or_404(Stage, id=post.id)
            context['stage'] = stage
            
        elif post.Catg == 'even_club':
            even_club = get_object_or_404(ÉvenClub, id=post.id)
            context['even_club'] = even_club
            
        elif post.Catg == 'even_social':
            even_social = get_object_or_404(ÉvenSocial, id=post.id)
            context['even_social'] = even_social
            
        elif post.Catg == 'transport':
            transport = get_object_or_404(Transport, id=post.id)
            context['transport'] = transport
            
        elif post.Catg == 'recommandation':
            recommandation = get_object_or_404(Recommandation, id=post.id)
            context['recommandation'] = recommandation

        return context



@login_required
@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.author:
        Notification.objects.create(
            notification_type=Notification.LIKE,
            user=instance.post.author,
            usercom=instance.author, 

            content_type=ContentType.objects.get_for_model(instance.post),
            object_id=instance.post.id
        )


User = get_user_model()  # Récupérer le modèle utilisateur actif
@login_required
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            notification_type=Notification.COMMENT,
            user=instance.post.author, 
            # Utilisez instance.post.author pour l'auteur du post
            usercom=instance.author, 
            content_type=ContentType.objects.get_for_model(instance.post),
            object_id=instance.post.id
        )


@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)
    
    # Mettre à jour is_read pour toutes les notifications non lues
    user_notifications.filter(is_read=False).update(is_read=True)
    
    return render(request, 'notifications.html', {'notifications': user_notifications})
from celery import shared_task
from datetime import datetime, timedelta

@shared_task
def delete_old_apps():
    # Récupérer la date il y a un mois
    one_month_ago = datetime.now() - timedelta(days=30)

    # Récupérer les applications créées il y a plus d'un mois
    old_apps = Post.objects.filter(created_at__lte=one_month_ago)

    # Supprimer les applications anciennes
    old_apps.delete()
