from django.db import models


class Brand(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField()

    def __str__(self):
        return self.title


class BrandDetails(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    strike_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.brand.title
