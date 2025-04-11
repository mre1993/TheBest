from django import forms
from .models import BestHomo, Place, Time, Field


class VoteForm(forms.Form):
    player = forms.ModelChoiceField(
        queryset=BestHomo.objects.all(),
        empty_label="Select a Best Homo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ParentSelectionForm(forms.ModelForm):
    """Form that includes BestHomo name + parent fields."""
    place_parent = forms.ModelChoiceField(
        queryset=Place.objects.filter(parent__isnull=True),
        empty_label="Select Place",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    time_parent = forms.ModelChoiceField(
        queryset=Time.objects.filter(parent__isnull=True),
        empty_label="Select Time Period",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    field_parent = forms.ModelChoiceField(
        queryset=Field.objects.filter(parent__isnull=True),
        empty_label="Select Field",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = BestHomo
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ChildSelectionForm(forms.Form):
    """Dropdown-based selection for child fields only."""
    place_child = forms.ModelChoiceField(
        queryset=Place.objects.none(),
        empty_label="Select Sub-Place",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    time_child = forms.ModelChoiceField(
        queryset=Time.objects.none(),
        empty_label="Select Specific Time",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    field_child = forms.ModelChoiceField(
        queryset=Field.objects.none(),
        empty_label="Select Sub-field",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        parent_selections = kwargs.pop("parent_selections", {})
        super().__init__(*args, **kwargs)

        if "place_parent" in parent_selections and parent_selections["place_parent"]:
            self.fields["place_child"].queryset = Place.objects.filter(parent_id=parent_selections["place_parent"])

        if "time_parent" in parent_selections and parent_selections["time_parent"]:
            self.fields["time_child"].queryset = Time.objects.filter(parent_id=parent_selections["time_parent"])

        if "field_parent" in parent_selections and parent_selections["field_parent"]:
            self.fields["field_child"].queryset = Field.objects.filter(parent_id=parent_selections["field_parent"])