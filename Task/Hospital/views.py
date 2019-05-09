from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from LocationHelper import getDistance
from .forms import *


# Create your views here.
#function get Citites in for hospital beacue use more one
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

#make the orderbased the result of the search
def order(request, bid):
    bank = get_object_or_404(Bank, id=bid)

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
        "old": r

    }
    if request.method == "POST":
        form = RequestBloodForm(request.POST)
        AvaiableBlood = bank.blooddonation_set.filter(blood_type=request.POST["blood_type"], donation_status="1",
                                                      blood_expiration__gt=datetime.now())
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
            quantity_blood = int(int(request.POST["quantity"]))
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


# =====================
#function get the avaiable quantity in bank
def GetAvaiableBlod(bank, type):
    avaiable = bank.blooddonation_set.filter(blood_type=type, donation_status="1",
                                             blood_expiration__gt=datetime.now())
    return avaiable.count()

#System will direct chose the bank based the near of the city
def order2(request):
    hospitals = Hospital.objects.all()
    # print(bank.BloodDonation_set.all())
    banks = Bank.objects.all()
    bank_avaiable = []

    req = RequestBlood()
    r = dict()
    r["blood_type"] = "o+"
    r["patients_status"] = "1"
    r["hospital"] = ""
    r["quantity"] = ""
    context = {
        "bloods": req.BLOOD_TYPE,
        "stauts": req.PATION_STATUS,
        "hosptals": hospitals,
        "old": r

    }
    if request.method == "POST":
        form = RequestBloodForm(request.POST)
        hospital = get_object_or_404(Hospital, id=request.POST["hospital"])
        if form.is_valid():
            for bank in banks:
                if GetAvaiableBlod(bank, request.POST["blood_type"]) >= int(request.POST["quantity"]):
                    bank_avaiable.append(bank)
            for index, bank in enumerate(bank_avaiable):  # for add disance
                bank.distance = round(getDistance(bank.city, hospital.city))
            near_bank = sorted(bank_avaiable, key=lambda tup: tup.distance)
            print(near_bank)
            if (near_bank):
                (req.bank, req.hospital, req.patients_status, req.blood_type, req.quantity) = (near_bank[0],
                                                                                               get_object_or_404(
                                                                                                   Hospital,
                                                                                                   id=
                                                                                                   request.POST[
                                                                                                       "hospital"]),
                                                                                               request.POST[
                                                                                                   "patients_status"],
                                                                                               request.POST[
                                                                                                   "blood_type"],
                                                                                               request.POST["quantity"]
                                                                                               )

                AvaiableBlood = near_bank[0].blooddonation_set.filter(blood_type=request.POST["blood_type"],
                                                                      donation_status="1",
                                                                      blood_expiration__gt=datetime.now())

                quantity_blood = int(int(request.POST["quantity"]))
                deleteBlood = AvaiableBlood[0:quantity_blood].values_list("id", flat=True)
                BloodDonation.objects.filter(id__in=list(deleteBlood)).delete()
                req.save()
                messages.success(request, "sucess Request Blood -- (%s) -- From Bank %s " %
                                 (request.POST["blood_type"],
                                  near_bank[0].name)
                                 )
                return redirect("/hospital/")


            else:
                messages.error(request, "no Bank Have the request of %s Quantity %s " % (
                request.POST["blood_type"], request.POST["quantity"]))
                return redirect("/hospital/")

        else:
            messages.error(request, form.errors)

            context["old"] = request.POST
            return render(request, "Hospital/OrderForm2.html", context)

    else:
        return render(request, "Hospital/OrderForm2.html", context)


#function do the request
def do_request(req):
    banks = Bank.objects.all()
    bank_avaiable = []
    for bank in banks:
        if GetAvaiableBlod(bank, req.blood_type ) >= int(req.quantity):
            bank_avaiable.append(bank)
    for index, bank in enumerate(bank_avaiable):  # for add disance
        bank.distance = round(getDistance(bank.city, req.hospital.city))
    near_bank = sorted(bank_avaiable, key=lambda tup: tup.distance)
    print(near_bank)
    if (near_bank):
        AvaiableBlood = near_bank[0].blooddonation_set.filter(blood_type=req.blood_type,
                                                              donation_status="1",
                                                              blood_expiration__gt=datetime.now())

        quantity_blood = int(req.quantity)
        deleteBlood = AvaiableBlood[0:quantity_blood].values_list("id", flat=True)
        BloodDonation.objects.filter(id__in=list(deleteBlood)).delete()
        req.bank = near_bank[0]
        req.request_status = "1"
        req.save()
    else:
        req.request_status = "0"
        req.save()

#System will Save order until reach to 10 the sytem will run to do requestes
def order3(request):
    hospitals = Hospital.objects.all()
    # print(bank.BloodDonation_set.all())
    banks = Bank.objects.all()
    bank_avaiable = []

    req = RequestBlood()
    r = dict()
    r["blood_type"] = "o+"
    r["patients_status"] = "1"
    r["hospital"] = ""
    r["quantity"] = ""
    context = {
        "bloods": req.BLOOD_TYPE,
        "stauts": req.PATION_STATUS,
        "hosptals": hospitals,
        "old": r

    }
    if request.method == "POST":
        form = RequestBloodForm(request.POST)
        hospital = get_object_or_404(Hospital, id=request.POST["hospital"])
        x = Bank.objects.first()
        if form.is_valid():
                (req.hospital, req.patients_status, req.blood_type, req.quantity,request_status) = (
                                                                                               get_object_or_404(
                                                                                                   Hospital,
                                                                                                   id=
                                                                                                   request.POST[
                                                                                                       "hospital"]),
                                                                                               request.POST[
                                                                                                   "patients_status"],
                                                                                               request.POST[
                                                                                                   "blood_type"],
                                                                                               request.POST["quantity"],
                                                                                                "2"
                                                                                               )
                req.save()
                reqs = RequestBlood.objects.filter(request_status="2")
                if reqs.count() >= 10:
                    for r in reqs:
                        do_request(r)


                messages.success(request, "sucess Request Blood -- (%s) -- From Bank %s " %
                                 (request.POST["blood_type"],
                                  "will Chose")
                                 )
                return redirect("/hospital/")

        else:
            messages.error(request, form.errors)

            context["old"] = request.POST
            return render(request, "Hospital/OrderForm3.html", context)

    else:
        return render(request, "Hospital/OrderForm3.html", context)

