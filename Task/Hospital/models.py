from django.core.validators import MinValueValidator

from Doner.models import *


# Create your models here.
class Hospital(models.Model):
    CITIES = (
        ("Cairo ,Egypt", "Cairo"),
        ("Mansoura ,Egypt", "Mansoura"),
        ("Arish ,Egypt", "Arish"),
        ("Ismailia ,Egypt", "Ismailia"),
        ("Alexandria ,Egypt", "Alexandria"),
        ("Aswan ,Egypt", "Aswan"),
        ("Asyut ,Egypt", "Asyut"),
        ("Beheira ,Egypt", "Damanhur"),
        ("Beni Suef ,Egypt", "Beni Suef"),
        ("Faiyum ,Egypt", "Faiyum"),
        ("Gharbia ,Egypt", "Tanta"),
        ("Giza ,Egypt", "Giza"),
        ("Kafr El Sheikh ,Egypt", "Kafr El Sheikh"),
        ("Matruh ,Egypt", "Marsa Matruh "),
        ("Monufia ,Egypt", "Shibin El Kom"),

    )
    name = models.CharField(max_length=250)
    address = models.TextField()
    city = models.CharField(max_length=250, choices=CITIES)

    def __str__(self):
        return self.name


class RequestBlood(models.Model):
    BLOOD_TYPE = (
        ("o+", "O+"),
        ("o-", "O-"),
        ("a+", "A+"),
        ("a-", "A-"),
        ("b+", "B+"),
        ("ab+", "AB+"),
        ("ab-", "AB-"),
    )
    REQUEST_STATUS = (
        ("0", "REJECT"),
        ("1", "ACCEPT"),
    )
    PATION_STATUS = (
        ("1", "Normal"),
        ("2", "Urgent"),
        ("3", "Immediate"),
    )
    blood_type = models.CharField(max_length=4, choices=BLOOD_TYPE)
    request_status = models.CharField(max_length=1, choices=REQUEST_STATUS, editable=False, default="0")
    patients_status = models.CharField(max_length=1, choices=PATION_STATUS)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(10)])
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.blood_type
