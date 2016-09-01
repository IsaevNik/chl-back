# coding: utf-8

from django.db import models

from task import Task


class PointBlank(models.Model):
    REPORT = 1
    INTERVIEW = 2
    FOTO = 3

    TYPE_CHOICES = (
        (REPORT, 'Отчёт'),
        (INTERVIEW, 'Опрос'),
        (FOTO, 'Фото')
    )

    task = models.ForeignKey(Task, 
                             related_name="blanks", 
                             on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    order = models.IntegerField()
    expl_image = models.CharField(blank=True, null=True, max_length=100)
    content = models.TextField()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ('order',)
