from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Article, Comment
from django.urls import reverse_lazy
from .forms import CommentForm


class ArticleListView(LoginRequiredMixin, ListView):

    model = Article
    template_name = 'article_list.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user
        return context


@login_required(login_url='login')
def ArticleDetailView(request, slug):

    template_name = 'article_detail.html'
    article = get_object_or_404(Article, id=slug)
    comments = article.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            return HttpResponseRedirect(request.path_info)

    else:
        comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'user': request.user,
    }
    return render(request, template_name, context)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Article
    fields = ('title', 'body')
    template_name = 'article_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):

    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body',)
    login_url = 'login'

    def form_valid(self, form):

        form.instance.author = self.request.user
        return super().form_valid(form)


