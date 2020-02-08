from django.db import models

class Anchor(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(default='',upload_to='VDJ_fasta')

    def __str__(self):
        return self.description


# class VDJFile(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#
# class Anchor_Dict(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
