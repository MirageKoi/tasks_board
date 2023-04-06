from django.db import models

 
class CardModel(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('In QA', 'In QA'),
        ('Ready', 'Ready'),
        ('Done', 'Done'),
    ]
    title = models.CharField(max_length=64)
    text = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='New')
    creator = models.ForeignKey('users.UserModel', related_name='cards', on_delete=models.CASCADE)
    implementor = models.ForeignKey('users.UserModel', related_name='implementors', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title
    

    class Meta:
        ordering = ['created']




