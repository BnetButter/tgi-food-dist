from django.db import models
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField


class DistributionCenterType(models.TextChoices):
    FOOD_BANK = "food_bank", "Food Bank"
    URBAN_FARM = "urban_farm", "Urban Farm"
    INDIVIDUAL_CONTRIBUTOR = "individual_contributor", "Individual Contributor"
    OTHER = "other", "Other"

# Create your models here.
class DistributionCenter(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    center_name = models.CharField(max_length=255)
    poc_email = models.EmailField()
    poc_phone_number = PhoneNumberField(max_length=255)
    distribution_type = models.CharField(max_length=255, choices=DistributionCenterType.choices)
    other_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.center_name} - {self.address}"


class InventoryItem(models.Model):
    distribution_center = models.ForeignKey(DistributionCenter, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
