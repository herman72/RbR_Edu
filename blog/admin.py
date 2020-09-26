from django.contrib import admin

from .models import Post, Comment, UserBlog


class CommentInline(admin.StackedInline):
    model = Comment
    readonly_fields = ['author_comment', 'text', 'created_time', 'post']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_time')
    fields = ['title', 'author', 'created_time', 'text']
    # def
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(UserBlog)
