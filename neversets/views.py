from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone

import json
import os

from friendship.models import Friend, bust_cache

from .forms import (RequestFriend,
Accept, Decline, Unfriend)
from .models import UserProfile
def redirect(request):
    return HttpResponseRedirect('/profile/')

@login_required
def profile(request):
    bust_cache('friends', request.user.pk)
    bust_cache('requests', request.user.pk)
    user_info = {
    'accept': Accept(),
    'decline': Decline(),
    'request':RequestFriend(),
    'unfriend': Unfriend(),
    'friends': Friend.objects.friends(request.user),
    'requests': Friend.objects.unrejected_requests(user=request.user),
    'count': Friend.objects.unrejected_request_count(user=request.user),
    'sent_requests': Friend.objects.sent_requests(user=request.user),
    }
    return render(request, 'neversets/profile.html', user_info)

#--------FRIEND REQUEST HANDLING--------#

@login_required
def send_request(request):
    if request.method == "POST":
        data = request.POST['email']
        to_json = {'message' : ''}
        try:
            other_user = UserProfile.objects.get(email=data)
            if Friend.objects.are_friends(request.user, other_user):
                to_json['message'] = 'You\'re already friends with ' + data 
            else:
                try:
                    Friend.objects.add_friend(request.user, other_user)
                    to_json['message'] = 'Friend request sent'
                except:
                    to_json['message'] = 'There was an error sending the friend request.'
        except UserProfile.DoesNotExist:
            to_json['message'] = 'Sorry, no user with email "' + data + '" was found in the database'
        return HttpResponse(json.dumps(to_json), content_type="application/json")
    return HttpResponseRedirect('/profile/')

@login_required
def accept_friend(request):
    if request.method == "POST":
        form = Accept(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            for i in Friend.objects.unrejected_requests(request.user):
                if str(i.from_user.email) == data['accept_user']:
                    i.accept()
                    return HttpResponseRedirect('/profile/')
                else:
                    pass
            return HttpResponse('couldn\'t find match')
        else:
            return HttpResponse('form invalid')
    else:
        return HttpResponse('request not post')

@login_required
def reject_friend(request):
    if request.method == "POST":
        form = Decline(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            for i in Friend.objects.unrejected_requests(request.user):
                if str(i.from_user) == data['decline_user']:
                    i.reject()
                else:
                    pass
            return HttpResponseRedirect('/profile/')

@login_required
def unfriend(request):
    if request.method == "POST":
        form = Unfriend(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            for i in Friend.objects.friends(request.user):
                if str(i.email) == data['unfriend_user']:
                    Friend.objects.remove_friend(i, request.user)
                else:
                    pass
            return HttpResponseRedirect('/profile/')
        else:
            return HttpResponseRedirect('/profile/')
    else:
        return HttpResponseRedirect('/profile/')

#-----LOCATION UPDATES-----#

@login_required
@csrf_exempt
def update_location(request):
    if request.method == "POST":
        user = request.user
        try:
            if user.city != request.POST['city'] or user.country != request.POST['country']:
                user.city = request.POST['city']
                user.country = request.POST['country']
                user.history_set.create(city=user.city, country=user.country)
                user.save()
                return HttpResponse(user.first_name + " is now in " + user.city + ', '+ user.country)
            else:
                return HttpResponse('Nothing to update')
        except UserProfile.DoesNotExist:
            return HttpResponse('No such user')
    else:
        return HttpResponseRedirect('/main/')