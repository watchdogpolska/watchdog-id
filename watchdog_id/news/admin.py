from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''
        Admin View for Post
    '''
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'status', 'published_at')
    list_filter = ('published_at', 'status')
    search_fields = ('title', 'content')
