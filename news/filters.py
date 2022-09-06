import django_filters
from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import Post, Category, PostCategory


class PostFilter(FilterSet):

    categ = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Without category'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'state': ['exact'],
            'datetime': ['gt'],
        }

class PostCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = PostCategory
        fields = ['category']