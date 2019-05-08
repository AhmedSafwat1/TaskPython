from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from LocationHelper import getDistance
from .forms import *


# Create your views here.
def getCities():
    hospital = Hospital()
    return hospital.CITIES


def index(request):
    context = {
        "cities": getCities(),
        "citySelect": ""
    }
    return render(request, "Hospital/Home.html", context)


def search(request):
    banks = Bank.objects.all()
    print(banks)
    for index, bank in enumerate(banks):  # for add disance
        bank.distance = round(getDistance(bank.city, request.GET["city"]))
    near_bank = sorted(banks, key=lambda tup: tup.distance)
    context = {
        "cities": getCities(),
        "near_bank": near_bank,
        "banks": banks,
        "flag": True,
        "citySelect": request.GET["city"]
    }
    print(near_bank)
    return render(request, "Hospital/Home.html", context)


def order(request, bid):
    bank = get_object_or_404(Bank, id=bid)
    AvaiableBlood = bank.blooddonation_set.filter(blood_type="o+", donation_status="1",
                                                  blood_expiration__gt=datetime.now())

    hospitals = Hospital.objects.all()
    # print(bank.BloodDonation_set.all())
    req = RequestBlood()
    r = dict()
    r["blood_type"] = "o+"
    r["patients_status"] = "1"
    r["hospital"] = ""
    r["quantity"] = ""
    context = {
        "bank": bank,
        "bloods": req.BLOOD_TYPE,
        "stauts": req.PATION_STATUS,
        "hosptals": hospitals,
        "old":r

    }
    if request.method == "POST":
        form = RequestBloodForm(request.POST)
        if form.is_valid() and AvaiableBlood.count() >= int(request.POST["quantity"]):
            (req.bank, req.hospital, req.patients_status, req.blood_type, req.quantity) = (bank,
                                                                                           get_object_or_404(Hospital,
                                                                                                             id=
                                                                                                             request.POST[
                                                                                                                 "hospital"]),
                                                                                           request.POST[
                                                                                               "patients_status"],
                                                                                           request.POST["blood_type"],
                                                                                           request.POST["quantity"]
                                                                                           )
            quantity_blood = int(int(request.POST["quantity"])) - 1
            deleteBlood = AvaiableBlood[0:quantity_blood].values_list("id", flat=True)
            BloodDonation.objects.filter(id__in=list(deleteBlood)).delete()
            req.save()
            messages.success(request, "sucess Request Blood -- (%s) --  " % (request.POST["blood_type"]))
            return redirect("/hospital/")

        else:
            messages.error(request, form.errors)

            if request.POST["quantity"] and AvaiableBlood.count() < int(request.POST["quantity"]):
                print("hi")
                messages.error(request, "Quanty in the Bank not enough for the request -- can chose another near one")
                return redirect("/hospital/")
            context["old"] = request.POST
            return render(request, "Hospital/OrderForm.html", context)

    else:
        return render(request, "Hospital/OrderForm.html", context)
