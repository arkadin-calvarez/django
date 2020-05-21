from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

class ContactForm(forms.Form):
    minion = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=True,label='Your e-mail address')

def minion_form(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            return HttpResponseRedirect('/minion_form?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'minion_form.html', {'form': form, 'submitted': submitted})