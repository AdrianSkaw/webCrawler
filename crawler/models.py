from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=50, blank=False, )
    url = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title


class BrandDetails(models.Model):
    title = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.FloatField(blank=False)
    strike_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title.title
