from django import forms
from .models import Post, Block


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
            if field.name == "content":
                field.field.widget.attrs["rows"] = "5"


    class Meta:
        model = Post
        exclude = ["user"]


class BlockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Block
        exclude = ["blocker"]