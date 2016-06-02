from __future__ import unicode_literals

from django.db import models


class Message(models.Model):

    title = models.CharField(max_length=50)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    seq = models.PositiveSmallIntegerField(default=0)

    # for redirect to just created message
    # def get_url(self):
    #     return '/message/%d/' % self.pk

    def __unicode__(self):

        return self.title

    class Meta:
        db_table = 'messages'


class TreeOrderField(models.CharField):

    def pre_save(self, model_instance, add):

        if add:
            parent = (model_instance.parent or model_instance.message)

            if parent.seq < 1000:
                parent.seq += 1
                parent.save()

            else:
                pass

            value = '%s%03d' % (getattr(parent, self.attname, ''), parent.seq)[:255]
            setattr(model_instance, self.attname, value)

            return value

        return models.CharField.pre_save(self, model_instance, add)


class Comment(models.Model):

    text = models.CharField(max_length=200)
    added_at = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, default=1)
    seq = models.PositiveSmallIntegerField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child_set')
    path = TreeOrderField(max_length=255, blank=True)

    @property
    def level(self):
        return max(0, len(self.path) / 3 - 1) * ". . . "

    def __unicode__(self):
        return self.text

    class Meta:
        db_table = 'comments'
        ordering = ['path']
