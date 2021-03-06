from datetime import date
from agreements.models import Agreement
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render


def json_view(request):
    country = request.GET.get('country')
    negotiator = request.GET.get('negotiator')
    company = request.GET.get('company')
    last_5_years = range(date.today().year-5, date.today().year+1)
    query = Agreement.objects.filter(end_date__year__in=last_5_years)
    try:
        # if country:
        #     query = query.filter(company__country__id__in=[int(i) if i.isdigit() else i for i in country.split(',')])
        if negotiator:
            query = query.filter(negotiator__id__in=[int(i) if i.isdigit() else i for i in negotiator.split(',')])
        if company:
            query = query.filter(company__id__in=[int(i) if i.isdigit() else i for i in company.split(',')])
    except ValueError as e:
        return HttpResponseBadRequest("Please input correct data: " + e.message)

    result = dict()
    for year in last_5_years:
        year_query = query.filter(end_date__year=year)
        month_list = []
        for month in range(1, 13):
            month_list.append(year_query.filter(end_date__month=month).count())
        result[year] = month_list
    return JsonResponse(result)


def home(request):
    context = {'result': json_view(request).content}
    return render(request, 'agreements/home.html', context)

