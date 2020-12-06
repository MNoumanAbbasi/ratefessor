from django import forms


class AddReviewForm(forms.Form):
    range_widget = forms.widgets.NumberInput(attrs={'type': 'range', 'class': "custom-range", 'min': "1", 'max': "5"})
    workload = forms.IntegerField(label="Workload", widget=range_widget)
    learning = forms.IntegerField(label="Learning", widget=range_widget)
    grading = forms.IntegerField(label="Grading", widget=range_widget)
    review = forms.CharField(label="Review", max_length=50, widget=forms.Textarea)
