from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.forms.models import ModelForm
from .models import Post, Block, Profile, Comment, File

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    def has_view_permission(self, request: HttpRequest, obj = None) -> bool:
        return True
    
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.user)
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.user)
    
    def has_add_permission(self, request: HttpRequest, obj = None) -> bool:
        return  request.user.is_superuser


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']
    list_filter = ['created_at']
    search_fields = ['title', 'content']
    exclude = ['author']

    def has_view_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and not Block.objects.filter(blocked=request.user, blocker=obj.author.user).exists())

    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.author.user)
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.author.user)
    
    def has_add_permission(self, request: HttpRequest, obj = None) -> bool:
        return True
    
    def save_model(self, request: HttpRequest, obj: Post , form:ModelForm, change: bool) -> None:
       if obj is not change:
              obj.author = Profile.objects.get(user=request.user)

       super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'post','created_at']
    exclude = ['author']

    def has_view_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and not Block.objects.filter(blocked=request.user, blocker=obj.author.user).exists())
    
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.author.user)
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.author.user)
    
    def save_model(self, request: HttpRequest, obj: Comment , form:ModelForm, change: bool) -> None:
         if obj is not change:
                  obj.author = Profile.objects.get(user=request.user)
    
         super().save_model(request, obj, form, change)


class FileAdmin(admin.ModelAdmin):

    def has_view_permission(self, request: HttpRequest, obj = None ) -> bool:
        return request.user.is_superuser or (obj is not None and not Block.objects.filter(blocked=request.user, blocker=obj.post.author.user).exists())
    
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.post.author.user)
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.post.author.user)
    


class BlockAdmin(admin.ModelAdmin):
    
    def has_view_permission(self, request: HttpRequest, obj = None) -> bool:
        return True
    
    def has_change_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.blocker)
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return True
    
    def has_delete_permission(self, request: HttpRequest, obj = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.blocker)

admin.site.register(Post, PostAdmin)    
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(File, FileAdmin)