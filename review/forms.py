from django import forms


class AddReviewForm(forms.Form):
    semester = forms.ChoiceField(label='Semester', choices=[(x, x) for x in ['Fall', 'Spring', 'Summer']])
    year = forms.ChoiceField(label='Year', choices=[(x, x) for x in range(2000, 2020)])
    range_widget = forms.widgets.NumberInput(
        attrs={'type': 'range', 'class': "custom-range w-25 form-control", 'min': "1", 'max': "5"})
    workload = forms.IntegerField(label="Workload (1-5)", widget=range_widget)
    learning = forms.IntegerField(label="Learning (1-5)", widget=range_widget)
    grading = forms.IntegerField(label="Grading (1-5)", widget=range_widget)
    review = forms.CharField(label="Review", max_length=150, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '3'}))
