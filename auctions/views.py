from pickle import TRUE
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


from .models import Conversation, Message

from .models import User

from .models import Comments, Auction_listing, Whatchlist, Bids, Category

# separate form file used
from .forms import Auction_listingForm, CommentsForm, BidsForm

# for decorators
from django.contrib.auth.decorators import login_required

#for datetime
import datetime

#for Max bid
from django.db.models import Max


def index(request):
    if request.user.is_authenticated:
        watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #for wahtlistcount in heading
        return render(request, "auctions/index.html", {
                "items": Auction_listing.objects.filter(actual=1),
                "watchlistcount": watchlistcount,
            }
            )

    else:
        return render(request, "auctions/index.html", {
            "items": Auction_listing.objects.filter(actual=1)
        }
        )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# My code below:

@login_required(login_url='/login')
def create_listing(request): 
    watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #for wahtlistcount in heading
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:                
        form = Auction_listingForm(request.POST, request.FILES)
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required            
            data = form.save(commit=False)
            data.current_price = form.cleaned_data["starting_bid"]
            data.ownerid = request.user
            data.winnerid = request.user
            data.save()
            form.save_m2m() #for ManytoManyField Django the save() method

            # redirect to a new URL:
            return render(request,'auctions/thanks.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Auction_listingForm()

        return render(request, 'auctions/create_listing.html', {'form': form,
                "watchlistcount": watchlistcount,})    

def entry(request, entryid):
    entry = Auction_listing.objects.get(id=entryid)  #select the item  
    categories = entry.category.all() #select after join in the Category table (multiple)                   
    print("entry", entry)
    start_bid = entry.starting_bid
    current_bid = entry.current_price
    print("entry.current_price", current_bid) 
    bids_sofar = Bids.objects.filter(listingid=entryid).count()
    comments = Comments.objects.filter(listingid=entryid)
    anchor = ""
    owner = False

    #if (entry.actual == 0):
        # return HttpResponseRedirect(reverse("entry_closed", args=(entryid,)))
        
    if request.user.is_authenticated:
        if  entry.ownerid == request.user:
            owner = True

        there_are_your_bids = Bids.objects.filter(listingid=entryid).filter(userid=request.user)
        if there_are_your_bids:
            your_current_bid = Bids.objects.filter(listingid=entryid).get(userid=request.user)
        else:
            your_current_bid = "you have not place any bid"
        bid_error =  0 #flag
        form_bids = BidsForm() #blank form 
        bid = ""  

        if request.method == 'POST' and 'whatchlist' in request.POST:
            # Finding flag "whatchlist" from the submitted form data
            whatchlist = int(request.POST["whatchlist"])
            user = request.user             
            if whatchlist==1: 
                w = Whatchlist(userid=user, listingid_id=entryid)                              
                w.save()
                print("Record saved")
            else:
                try:
                    w=Whatchlist.objects.filter(userid=user).get(listingid=entryid)
                    w.delete()
                    print("Record deleted successfully!")
                except:
                    print("Record doesn't exists") 

        elif request.method == 'POST' and 'bids' in request.POST:
            anchor = "bids"
            # create a form instance and populate it with data from the request: 
            form_bids_post = BidsForm(request.POST)                 
            # check whether it's valid:
            if form_bids_post.is_valid():
                # process the data in form.cleaned_data as required 
                bid = int(request.POST["bid"])
                #start_bid = Auction_listing.objects.filter(id=entryid).values()
                print("bid", bid)
                if (bids_sofar == 0 and bid >= start_bid) or (bids_sofar > 0 and  bid > current_bid):
                    if bids_sofar == 0 or not there_are_your_bids: #noone bid or no your bid
                        #insert your bid in Bids 
                        data = form_bids_post.save(commit=False)                            
                        data.userid = request.user 
                        data.listingid_id = entryid            
                        data.save() 
                        form_bids_post.save_m2m() #for ManytoManyField Django the save() method

                    else: #there_are_your_bids and bid > current_bid
                        #unpdate your bid in Bids 
                        your_current_bid.bid = bid
                        your_current_bid.save()  

                    #unpdate Auction_listing as current_price
                    print("update current price")
                    entry.current_price = bid
                    entry.winnerid = request.user
                    entry.save()
                    #update on the page:
                    your_current_bid = Bids.objects.filter(listingid=entryid).get(userid=request.user)
                    bids_sofar = Bids.objects.filter(listingid=entryid).count()
                else: 
                    print("bid is incorrect")
                    bid_error =  1 
                    form_bids = BidsForm(request.POST) #prepopulated form 
        
        elif request.method == 'POST' and 'comments' in request.POST:
            anchor = "comments"
            # create a form instance and populate it with data from the request:             
            form_comments_post = CommentsForm(request.POST)
            # check whether it's valid:
            if form_comments_post.is_valid():
                # process the data in form.cleaned_data as required            
                data = form_comments_post.save(commit=False)            
                data.userid = request.user 
                data.listingid_id = entryid            
                data.save()                             
        else:
            print("this was GET request") 

        # for both GET and POST we'll create a blank forms + prepopupated some data                    
        watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #number of items for this used
        watchlist = Whatchlist.objects.filter(listingid=entryid).filter(userid=request.user) #selected the row: this item, this user                          
        #data = {"inwatchlist": w} #prepopulate the whatchlist form with data from db
        #form_whatchlist = WhatchlistForm(data)
                
        form_comments = CommentsForm() #blank form        
        title = entry.listing_title  #for layout specifically 

        if (entry.actual == 0):
            return render(request, "auctions/entry_closed_work_on.html", { 
                "watchlistcount": watchlistcount, 
                "watchlist": watchlist,                      
                "entry": entry,
                "bids_sofar": bids_sofar, 
                "your_current_bid": your_current_bid, 
                "form_bids": form_bids, 
                "categories": categories,
                "comments": comments,
                "form_comments": form_comments, 
                "title": title, #for layout specifically 
                "bid_error": bid_error,
                "bid": bid,
                "anchor": anchor,
                "owner": owner,
            })        
        
        else:
            return render(request, "auctions/entry_workon.html", { 
                "watchlistcount": watchlistcount, 
                "watchlist": watchlist,                      
                "entry": entry,
                "bids_sofar": bids_sofar, 
                "your_current_bid": your_current_bid, 
                "form_bids": form_bids, 
                "categories": categories,
                "comments": comments,
                "form_comments": form_comments, 
                "title": title, #for layout specifically 
                "bid_error": bid_error,
                "bid": bid,
                "anchor": anchor,
                "owner": owner,
            }
            ) 

    # not authenticated user
    else:
        print("not authenticated user")   
        if (entry.actual == 0):
            return HttpResponseRedirect(reverse("entry_closed", args=(entryid,)))
        else:
            return render(request, "auctions/entry.html", {        
                "entry": entry,
                "categories": categories,
                "comments": comments,
            }
            ) 


# If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.

# If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.

@login_required(login_url='/login')
def entry_closed(request, entryid):
    entry = Auction_listing.objects.get(id=entryid)  #select the item
    categories = entry.category.all() #select after join in the Category table (multiple) 
    comments = Comments.objects.filter(listingid=entryid)              
    
    if request.method == 'POST':                          
        # Finding flag "close" from the submitted form data
        close = int(request.POST["close"])                     
        if close==1: 
            # in Auction_listing actual=0
            entry.actual = 0
            entry.save()
            print("Auction closed")
        else:
            print("Something went wrong")
    else:
        print("this was GET request on closed") 
    
    # for both GET and POST 

    if  request.user == entry.ownerid:
        status = "owner"
    elif request.user == entry.winnerid:
        status = "winner"
    else:
        status = "other" 

    title = entry.listing_title  #for layout  specifically 
    watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #number of items for this used           
    return render(request, "auctions/entry_closed.html", {
        "watchlistcount": watchlistcount,                        
        "entry": entry,
        "categories": categories,
        "comments": comments,
        "title": title, #for layout  specifically
        "status": status,
    }
    ) 

@login_required(login_url='/login')
def my_listings(request):
    
        watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #for wahtlistcount in heading
        return render(request, "auctions/my_listings.html", {
                "items": Auction_listing.objects.filter(ownerid=request.user),
                "watchlistcount": watchlistcount,
            }
            )

@login_required(login_url='/login')
def my_watchlist(request):

        watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #for wahtlistcount in heading
        print(Auction_listing.objects.filter(ownerid=request.user))
        print(Whatchlist.objects.filter(userid=request.user))
        #items = Auction_listing.objects.filter(id__in=Whatchlist.objects.filter(userid=request.user))
        #items = Whatchlist.objects.filter(userid=request.user).filter(listingid=22)
        #SELECT * FROM Whatchlist JOIN Auction_listing ON
        # Auction_listing.id=Whatchlist.listingid
        #WHERE Whatchlist.userid=request.user
        
        user_wl = Whatchlist.objects.filter(userid=request.user)

        # List comprehension to extract the id's
        items1 = [item.listingid for item in user_wl]
        items2 = [item.id for item in items1]

        # Get AuctionListings
        items = Auction_listing.objects.filter(id__in=items2)
        
        print(items)
        #items = Auction_listing.objects.filter(ownerid=request.user)       
        return render(request, "auctions/my_watchlist.html", {
                "items": items,
                "watchlistcount": watchlistcount,
            }
            )    

def categories(request):
    if request.user.is_authenticated:
        watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #for wahtlistcount in heading
        return render(request, "auctions/categories.html", {
            "items": Category.objects.all(),
            "watchlistcount": watchlistcount,
        }
        )

    else:
        return render(request, "auctions/categories.html", {
            "items": Category.objects.all(),        
    }
    )

def category_listings(request, categoryid): 
    if request.user.is_authenticated:
        watchlistcount = Whatchlist.objects.filter(userid=request.user).count() #for wahtlistcount in heading   
        return render(request, "auctions/category_listings.html", {
            "items": Auction_listing.objects.filter(actual=1).filter(category=categoryid),
            "watchlistcount": watchlistcount,
        }
        )  
    else:  
        return render(request, "auctions/category_listings.html", {
            "items": Auction_listing.objects.filter(actual=1).filter(category=categoryid),
            
        }
        )                  

@login_required(login_url='/login')
def conversations(request):
    user = request.user
    conversations = user.conversations.all()
    return render(request, 'chat/conversations.html', {'conversations': conversations})

@login_required(login_url='/login')
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.message_set.all()
    return render(request, 'chat/conversation.html', {'conversation': conversation, 'messages': messages})

@login_required(login_url='/login')
def send_message(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        sender = request.user
        content = request.POST['content']
        Message.objects.create(conversation=conversation, sender=sender, content=content)
        return redirect('conversation', conversation_id=conversation_id)
