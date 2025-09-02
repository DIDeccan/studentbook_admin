from django.db import models

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "studentbookfrontend_class"
 
 