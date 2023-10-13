from django.shortcuts import render, HttpResponse, redirect
from .models import Friends, Messages
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer
from django.contrib.auth.models import User
from django.contrib import messages 
from userProfile.models import *

from .recommendBuddy import recommend_user_list


def get_user_list(id):
    user_object = UserProfile.objects.get(user=id)
    cur_summary = user_object.moving_summary_buffer

    users_except_cur = UserProfile.objects.exclude(user=id)

    user_dict = {}

    for item in users_except_cur:
        user_dict[item.user.username] = item.moving_summary_buffer

    print('inputs for recommendation system here - - - - - ')
    print(cur_summary)
    print('--------------------')
    print(user_dict)

    return cur_summary, user_dict



def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """

    try:
        user = User.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = User.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = User.objects.get(username=username)
    id = use.id
    return id


def index(request):
    """
    Return the home page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        messages.info(request, "Please Login first")
        return redirect("../userprofile/login/")
    else:
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
        return render(request, "chat/Base.html", {'friends': friends})


def search(request):
    """
    Search users page
    :param request:
    :return:
    """

    cur_summary, user_dict = get_user_list(request.user.id)
    users_list = recommend_user_list(cur_summary, user_dict)
    print(" recommended users here ")
    users = []
    for items in users_list:
        if items != '':
            print('here -------')
            fr = User.objects.get(username=items)
            users.append(fr)

    # users = list(Usery.objects.all())
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break

    if request.method == "POST":
        print("SEARCHING!!")
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.username:
                user_ls.append(user)
        return render(request, "chat/search.html", {'users': user_ls, })

    try:
        users = users[:10]
    except:
        users = users[:]

    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    return render(request, "chat/search.html", {'users': users, 'friends': friends})


def addFriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """

    username = request.user.username
    id = getUserId(username)
    friend = User.objects.get(username=name)
    curr_user = User.objects.get(id=id)
    print(curr_user.username)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("/social/search")


def chat(request, username):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    friend = User.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = User.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "chat/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
