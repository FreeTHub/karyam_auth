from django.db import models

# Create your models here.
class KeysDocument(models.Model):
    keyName = models.CharField(max_length=255, unique=True)
    valueName = models.TextField()

    class Meta:
        db_table = "keys_documents"  #