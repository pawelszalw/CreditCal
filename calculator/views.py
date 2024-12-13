from django.shortcuts import render, redirect
from .models.credit_details import CreditDetails
from datetime import datetime


# Home page
def home(request):
    return render(request, 'calculator/home.html')


# New Loan page
def new_loan(request):
    if request.method == "POST":
        # Parse common fields
        principal = int(request.POST.get("principal"))
        term = int(request.POST.get("term"))

        # Interest rate handling
        use_separate_rates = request.POST.get("use_separate_rates") == "on"
        if use_separate_rates:
            bank_margin = float(request.POST.get("bank_margin"))
            base_interest_rate = float(request.POST.get("base_interest_rate"))
            current_interest_rate = bank_margin + base_interest_rate
        else:
            current_interest_rate = float(request.POST.get("current_interest_rate"))

        # Penalty details
        add_penalty_details = request.POST.get("add_penalty_details") == "on"
        penalty_rate = None
        penalty_start_date = None
        penalty_end_date = None
        penalty_start_month = None
        penalty_end_month = None

        if add_penalty_details:
            penalty_rate = request.POST.get("penalty_rate")
            penalty_rate = float(penalty_rate) if penalty_rate else None
            penalty_start_date = request.POST.get("penalty_start_date")
            penalty_end_date = request.POST.get("penalty_end_date")

            # Convert dates to months
            if penalty_start_date:
                penalty_start_month = (datetime.fromisoformat(penalty_start_date).year * 12 +
                                       datetime.fromisoformat(penalty_start_date).month)
            if penalty_end_date:
                penalty_end_month = (datetime.fromisoformat(penalty_end_date).year * 12 +
                                     datetime.fromisoformat(penalty_end_date).month)

        # Save data to session
        request.session['principal'] = principal
        request.session['term'] = term
        request.session['current_interest_rate'] = current_interest_rate
        request.session['penalty_rate'] = penalty_rate
        request.session['penalty_start_month'] = penalty_start_month
        request.session['penalty_end_month'] = penalty_end_month

        return redirect('overpayment')  # Redirect to overpayment page

    return render(request, 'calculator/new_loan.html')


# Overpayment page
def overpayment(request):
    # Retrieve session data
    principal = request.session.get('principal')
    term = request.session.get('term')
    bank_margin = request.session.get('bank_margin')
    base_interest_rate = request.session.get('base_interest_rate')
    penalty_rate = request.session.get('penalty_rate')
    penalty_start_month = request.session.get('penalty_start_month')
    penalty_end_month = request.session.get('penalty_end_month')

    # Initialize the loan object
    credit = CreditDetails(
        initial_principal=principal,  # TODO modify in HTML
        term=term,
        bank_margin=bank_margin,
        base_interest_rate=base_interest_rate,
        penalty_rate=float(penalty_rate) if penalty_rate else None,
        penalty_start_month=int(penalty_start_month) if penalty_start_month else None,
        penalty_end_month=int(penalty_end_month) if penalty_end_month else None,
    )

    # Render the overpayment page
    return render(request, 'calculator/overpayment.html', {'credit': credit})


# About page
def about(request):
    return render(request, 'calculator/about.html')


def my_loan(request):
    return render(request, "calculator/my_loan.html")