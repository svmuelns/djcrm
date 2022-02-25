from django.db import models

# We represent data structure of our web page in models.py

class Lead(models.Model): 
    first_name = models.CharField(max_length=20) # we created a field
    # CharField() restricts the filed to be character in a database
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
