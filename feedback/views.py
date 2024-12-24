from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback

def submit_feedback(request):
    if request.method == 'POST':
        try:
            feedback = Feedback.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                subject=request.POST['subject'],
                message=request.POST['message']
            )
            messages.success(request, 'Thank you for your feedback! We will review it shortly.')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error submitting your feedback. Please try again.')
            return redirect('contact')
    return redirect('contact')
