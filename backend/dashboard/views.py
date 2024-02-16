from django.shortcuts import render

# Create your views here.
def home(request):
    if request.method == "POST":
        pass
    return render(request, 'dashboard/dashboard.html')
