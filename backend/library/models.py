from django.db import models
from user.models import User



class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    price =models.DecimalField(max_digits=10 , decimal_places=2)
    available = models.BooleanField(default=True)


    def __str__(self):
        return self.title
    

class Purchase(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='purchases')
    book = models.ForeignKey(Book , on_delete=models.CASCADE , related_name='purchases')
    purchase_at = models.DateTimeField(default=True)

    def __str__(self):
        return f'{self.user} - {self.book.title}'
    


    