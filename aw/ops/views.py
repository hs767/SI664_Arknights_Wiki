from django.views import View
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime

from ops.models import Operator, Comment, Fav
from ops.forms import CommentForm
from ops.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class OperatorListView(OwnerListView):
    model = Operator
    template_name = "ops/operator_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            query = Q(name__contains=strval)
            #query.add(Q(clas__contains=strval), Q.OR)
            operator_list = Operator.objects.filter(query).select_related().order_by('-rarity')
        else :
            # try both versions with > 4 posts and watch the queries that happen
            operator_list = Operator.objects.all().order_by('-rarity')

        for op in operator_list:
            op.natural_updated = naturaltime(op.updated_at)
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_operators.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'operator_list' : operator_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)


class OperatorDetailView(OwnerDetailView):
    model = Operator
    template_name = "ops/operator_detail.html"
    def get(self, request, pk) :
        x = Operator.objects.get(id=pk)
        comments = Comment.objects.filter(operator=x).order_by('-updated_at')
        #ratings = Rating.objects.filter(operator=x).order_by('-updated_at')
        comment_form = CommentForm()
        #rating_form = RatingForm()
        context = { 'operator' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class OperatorCreateView(OwnerCreateView):
    model = Operator
    fields = ['name', 'gender', 'rarity', 'race', 'base_type_1', 'base_type_2', 'clas']


class OperatorUpdateView(OwnerUpdateView):
    model = Operator
    fields = ['name', 'gender', 'rarity', 'race', 'base_type_1', 'base_type_2', 'clas']

class OperatorDeleteView(OwnerDeleteView):
    model = Operator

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Operator, id=pk)
        comment = Comment(text=request.POST['comment'], num=request.POST['rating'], owner=request.user, operator=f)
        comment.save()
        return redirect(reverse('ops:operator_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ops/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        operator = self.object.operator
        return reverse('ops:operator_detail', args=[operator.id])

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Operator, id=pk)
        fav = Fav(user=request.user, operator=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Operator, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, operator=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
'''class RatingCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Operator, id=pk)
        rating = Rating(num=request.POST['num'], owner=request.user, operator=f)
        rating.save()
        return redirect(reverse('ops:operator_detail', args=[pk]))

class RatingDeleteView(OwnerDeleteView):
    model = Rating
    template_name = "ops/rating_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        operator = self.object.operator
        return reverse('ops:operator_detail', args=[operator.id])'''
