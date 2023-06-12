from django.forms import ModelForm
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # to create all fields in the specifed in the model
        fields = ['title', 'description', 'featured_image',
                  'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),  # to turn tags as a checkboxes
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class':'input'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            field.widget.attrs.update({'style': 'width: 100% !important;'})