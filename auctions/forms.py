from django import forms
from django.forms import ModelForm
from .models import Message

from .models import Auction_listing, Category, Comments, Whatchlist, Bids

class Auction_listingForm(ModelForm): 
    # category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)
    class Meta:
        model = Auction_listing
        fields = ['listing_title', 'picture', 'starting_bid', 'category', 'listing_description']       
        
        category = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        
        widgets = {
            'listing_title': forms.TextInput(attrs={
                'class':'title',
                'placeholder': 'title of the listing'
                }),

            'listing_description' : forms.Textarea(attrs={
                'placeholder': 'description of the listing'
                })
        }   

""" class WhatchlistForm(ModelForm):     
    class Meta:
        model = Whatchlist
        fields = ['inwatchlist']   """

class BidsForm(ModelForm):     
    class Meta:
        model = Bids
        fields = ['bid']          

class CommentsForm(ModelForm):     
    class Meta:
        model = Comments
        fields = ['comment']  

        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'your comments'
                }),            
                }     

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
