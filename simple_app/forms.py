from django import forms
from django.core.urlresolvers import reverse

from models import Message, Comment


class MessageForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

    title = forms.CharField(widget=forms.TextInput)
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        text = self.cleaned_data.get('text')
        if text is None or len(text) < 5:
            raise forms.ValidationError(u'Text must contains more than 5 characters')
        return self.cleaned_data

    def save(self):
        message = Message(**self.cleaned_data)
        message.save()
        return message


class CommentForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        text = self.cleaned_data.get('text')
        if text is None:
            raise forms.ValidationError(u"Text can't be empty")
        return self.cleaned_data

    def save(self):
        comment = Comment(**self.cleaned_data)
        comment.parent = ('%s-%03d' % (comment.parent.path, self.id, ))[:255]
        comment.save()
        return comment
