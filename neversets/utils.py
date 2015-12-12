from friendship.models import Friend
from django.core.mail import EmailMessage
from django.http import HttpResponse
import requests

def friends_update(user):
    email_text = ''
    mvd = []
    i = 0
    #Loop over all of the user's friends
    for friend in Friend.objects.friends(user):
        #Check if the friend has any location saved in the database. This should never be false
        if friend.history_set.all():
            #Only proceed if the latest field added to the table was added less than one week ago 
            if friend.history_set.latest("created_at").changed_less_than_one_week_ago():
                mvd.append("<strong>" + friend.first_name + " " + friend.last_name + "</strong><br>")
                for move in friend.history_set.all():
                    if move.changed_less_than_one_week_ago():
                        t = move.created_at
                        try:
                            mvd[i] += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;>> " + move.city + ", " + move.country + " [updated " + t.strftime('%d/%m/%Y') + "]<br>"
                        except TypeError: #in case the location is somehow accidentally set to "Null."
                            pass
                    else:
                        pass
                i += 1
            else:
                pass
        else: 
            pass
    if mvd:
        moves = '<br>'.join(mvd)
        email_text = '<h2>Sun Never Sets on Us</h2>' +\
            "<p>As of last week, your friends\' locations have changed as follows:</p>" +\
            moves +\
            "<br><em>Thanks for using Sun Never Sets on Us :)</em>"+\
            "<br>--<br>"+\
            "You have %s unanswered friend request/s<br>" % Friend.objects.unrejected_request_count(user) +\
            "You can unsubscribe from these emails at\
            <a href=\"http://sunneversetson.us\">http://sunneversetson.us</a>"
        
        message = EmailMessage(
            'SunNeverSets: Your Location Update', 
            email_text,
            'jonathan@sunneversetson.us', 
            [user.email], 
        )
        message.content_subtype = 'html'
        message.send()
