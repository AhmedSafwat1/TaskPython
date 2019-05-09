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
        ("2", "Append"),
    )
    PATION_STATUS = (
        ("1", "Normal"),
        ("2", "Urgent"),
        ("3", "Immediate"),
    )
    blood_type = models.CharField(max_length=4, choices=BLOOD_TYPE)
    request_status = models.CharField(max_length=1, choices=REQUEST_STATUS, default="2")
    patients_status = models.CharField(max_length=1, choices=PATION_STATUS)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    bank = models.ForeignKey(Bank,  blank=True, null=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        state = ""
        if self.request_status == "0":
            state = "Refues"
        elif self.request_status == "1":
            state = "Accept"
        else:
            state = "Append"

        return self.blood_type+" , "+state
