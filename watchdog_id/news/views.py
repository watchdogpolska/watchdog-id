from braces.views import SelectRelatedMixin
from django.utils.timezone import now
from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView

from .models import Post


class PostArchiveMixin(SelectRelatedMixin):
    model = Post
    date_field = "published_at"
    select_related = ['user', ]
    month_format = "%m"

    @property
    def allow_future(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(PostArchiveMixin, self).get_context_data(**kwargs)
        context['post_months'] = self.get_queryset().datetimes(self.date_field, "month")
        return context


class PostArchiveIndexView(PostArchiveMixin, ArchiveIndexView):
    allow_empty = True
    pass


class PostMonthArchiveView(PostArchiveMixin, MonthArchiveView):
    pass


class PostDetailView(PostArchiveMixin, DetailView):
    def get_queryset(self, *args, **kwargs):
        qs = super(PostDetailView, self).get_queryset(*args, **kwargs)
        if not self.allow_future:
            qs = self.filter(published_at_gte=now())
        return qs
