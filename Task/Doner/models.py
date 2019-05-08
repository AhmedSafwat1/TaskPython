from datetime import datetime, timedelta

from django.core.mail import EmailMessage
from django.core.validators import MinLengthValidator, ValidationError
from django.db import models


# Create your models here.

class Doner(models.Model):  # Doner model
    national_id = models.CharField(max_length=14, validators=[MinLengthValidator(14)])
    name = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Bank(models.Model):  # Bank model
    CITIES = (
        ("Cairo ,Egypt", "Cairo"),
        ("Mansoura ,Egypt", "Mansoura"),
        ("Arish ,Egypt", "Arish"),
        ("Ismailia ,Egypt", "Ismailia")
    )

    city = models.CharField(max_length=250, choices=CITIES)
    name = models.CharField(max_length=250)
    address = models.TextField()

    def __str__(self):
        return self.name


# custome validator for valid enter the right date for last donate
def validate_last_donate_date(date):
    if date > datetime.now().date():
        raise ValidationError("The date cannot be in the Future!")
    else:
        return date


class BloodDonation(models.Model):  # relation betwean user and bank blood
    BLOOD_TYPE = (
        ("o+", "O+"),
        ("o-", "O-"),
        ("a+", "A+"),
        ("a-", "A-"),
        ("b+", "B+"),
        ("ab+", "AB+"),
        ("ab-", "AB-"),
    )
    TEST_STATUS = (
        ("0", "NAGATIVE"),
        ("1", "PPSTIVE"),
    )
    DONER_STATUS = (
        ("1", "More Then 3 Month"),
        ("0", "Less Then 3 Month"),
    )
    DONATION_STATUS = (
        ("1", "ACCEPT"),
        ("0", "REFUSE"),
    )

    blood_type = models.CharField(max_length=4, choices=BLOOD_TYPE)
    blood_expiration = models.DateTimeField(default=datetime.now() + timedelta(days=60), editable=False)
    test_state = models.CharField("Virus Test", max_length=1, choices=TEST_STATUS)
    doner_status = models.CharField("Last Donate ", max_length=1, choices=DONER_STATUS, editable=False, default="1")
    donation_status = models.CharField(max_length=1, choices=DONATION_STATUS, editable=False, default="1")
    description = models.TextField(null=True, blank=True, editable=False)
    doner = models.ForeignKey(Doner, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    last_donate_date = models.DateField(validators=[validate_last_donate_date])

    # send mail if state for donation false
    def save(self):
        # ========================
        # get the data and check if valid or not
        TimeNow = datetime.now().date()
        delta = TimeNow - self.last_donate_date
        print(delta)
        self.doner_status = "0" if (int(delta.days) < 90) else "1"
        # =====================
        desc = " "
        TestState = "is Nagative"
        if self.test_state == "1":
            self.donation_status = "0"
            TestState = "is Postive"
            desc = "you Test is Postive\n \t \t"
        elif self.doner_status == "0":
            self.donation_status = "0"
            desc += " you doante in " + str(self.last_donate_date) + " Less Then 3 Month "
        else:
            self.donation_status = "1"
        self.description = desc
        if self.donation_status == "0":
            state = "no more Then 3 Month " if self.test_state == "1" else "yes Less Then 3 Month"
            (name, type, state, bank, desc) = self.doner.name, self.blood_type, state, self.bank.name, self.description
            message = """
                Hello %s
                =================================
                You blood type  is %s
                You donated soon %s
                want To donate to %s
                Test State %s
                The Donation Application refuse :
                 ** %s
                =================================
                Thanks  -@SAFWAT-
                   
            """ % (name, type, state, bank, TestState, desc)
            email = EmailMessage('Donation rejection', message, to=[self.doner.email])
            email.send()
        super().save()

    def __str__(self):
        x = self.blood_type + ", Accept" if self.donation_status == "1" else self.blood_type + ",Refuse And Send The Mails for Reason"
        return x
