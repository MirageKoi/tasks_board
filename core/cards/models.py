from django.db import models


class CategoryModel(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.title

    
class CardModel(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    creator = models.ForeignKey('users.UserModel', related_name='cards', on_delete=models.CASCADE)
    implementor = models.ForeignKey('users.UserModel', related_name='implementors', on_delete=models.PROTECT, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title
    

    class Meta:
        ordering = ['created']




