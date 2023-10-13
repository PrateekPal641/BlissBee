# views.py
from http.client import HTTPResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages  # Import the messages module
from .models import *
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from django.conf import settings
from .chatbuddy import *
from .articlebuddy import pp_generation
from .scenariobuddy import *
from .journalbuddy import quote_generation
from .fitnessbuddy import * 
from .utils import *
import re
import random

import logging
from array import array


logger = logging.getLogger(__name__)



daily_activities = ['Sleep', 'Meditate', 'Yoga']
feelings = ["Happy", "Sad", "Excited", "Angry", "Confused", "Content", "Surprised", "Bored"]



def register(request):
    if request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Already logged in.")
        return redirect('../dashboard') 
    if request.method == 'POST':
        # Get data from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        status = request.POST.get('status')
        dob = request.POST.get('dob')

        if not (username and password and dob):
            return redirect('../register')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('../register')
 
       
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.get_or_create(user=user, date_of_birth = dob, gender=gender, relationship_status = status)
        logger.info("---  User registered and logged in ---")
        login(request, user)

        return redirect('../dashboard')  # Redirect to the home page or a success page

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Already logged in.")
        return redirect('../dashboard') 

    if request.method == 'POST':
        # Get data from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            logger.info("---  User logged in ---")
            login(request, user)
            return redirect('../dashboard')  # Redirect to the home page or a success page
        else:
            messages.info(request, "Enter valid Credentials")
    return render(request, 'login.html')


def dashboard(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Please login first.")
        return redirect('../login')  # Redirect to your login URL
    user = request.user
    username = user.username
    dob = user.userprofile.date_of_birth

    # current_date = timezone.now().date()
    # activity_list = Activity.objects.filter(user=user, date=current_date)

    # if not activity_list:
    #     for act_name in daily_activities:
    #         new_activity = Activity.objects.create(
    #             name=act_name,
    #             date=current_date,
    #             status='Pending',
    #             user=user
    #         )
    # activity_list = Activity.objects.filter(user=user, date=current_date)
    

    return render(request, 'dashboard.html', {'username': username, 'dob': dob})

def custom_logout(request):
    logout(request)
    return redirect('../login')


def add_material(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Please login first.")
        return redirect('../login')  # Redirect to your login UR
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        link = request.POST.get('link')
        feeling_ids = request.POST.getlist('feeling_ids')
        if title and content and link:
            material = Material.objects.create(title=title, content=content, link=link)
            material.feelings.set(feeling_ids)
            return redirect('../dashboard')  # Redirect to a page that lists all materials

    return render(request, 'add_material.html', {'feelings': Feeling.objects.all()})


def meditate(request):
    return render(request, 'meditate.html')

def scenario_view(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Please login first.")
        return redirect('../login')
    logger.info("---  Providing a scenario to the user -----")
    user_object = UserProfile.objects.get(user=request.user.id)
    gender = user_object.gender
    status = user_object.relationship_status
    dob= user_object.date_of_birth
    age = calculate_age(dob)
    
    m_illness = random.choice(feelings)
    if user_object.illness != "":
        m_illness = user_object.illness
    scenario = scene_generation(m_illness, gender, age, status)
    # scenario = scenario.split(":")[1]
    # scenario = json.dumps(scenario)

    past_scenario_list = ScenarioFeedback.objects.all()


    heading_pattern = r"Scenario Heading:\s*(.*)"
    content_pattern = r"Scenario:\s*(.*)"

    # # Search for the heading and content using regex
    heading_match = re.search(heading_pattern, scenario)
    content_match = re.search(content_pattern, scenario, re.DOTALL)  # Use re.DOTALL to match across multiple lines
    
    # print("hello")
    # print(heading_match.group(1).strip(),'------------------', content_match.group(1).strip())
    
    context ={
        'scenario': content_match.group(1).strip(),
        'scenario_heading': heading_match.group(1).strip(),
        'past_scenario_list': past_scenario_list
    }

    return render(request, 'scenario.html', context)

@csrf_exempt
def scenario_feedback_view(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Get the user's message from the JSON data
            scenario = data.get("scenario", "")
            scenario_heading = data.get("scenario_heading", "")
            response = data.get("response", "")
            scenario = scenario.strip('"')

            m_illness = random.choice(feelings)
            if request.user.userprofile.illness != "":
                m_illness = request.user.userprofile.illness

            feedback=answer_evaluation(m_illness, response, scenario)
            logger.info("---  Evaluation user response on given scenario -----")

            logger.info(scenario)
            logger.info("------------------------------------")
            logger.info(scenario_heading)
            logger.info("------------------------------------")
            logger.info(response)
            logger.info("------------------------------------")
            logger.info(feedback)

            # Prepare a response (e.g., chatbot response)
            

            rating_pattern = r'Rating in integer:\s+(\d+)'

            start_index = feedback.find("Evaluation Feedback:")
            end_index = feedback.find("Rating in integer:")

            # Extract the text between the two substrings
            if start_index != -1 and end_index != -1:
                extracted_text = feedback[start_index + len("Evaluation Feedback:"):end_index].strip()
            else:
                extracted_text = "Text not found"

            
            # Search for the rating pattern in the text
            match = re.search(rating_pattern, feedback)

            # Check if a match is found
            rating = 1
            if match:
                # Extract the rating value from the match
                rating = int(match.group(1))
            
            response_data = {
                "scenario": scenario,
                "response": response,
                "feedback": extracted_text,
                "rating": rating
            }
            
            scenario_feedback = ScenarioFeedback.objects.create(
                user=request.user,
                title = scenario_heading,
                scenario=scenario,
                response=response,
                feedback=extracted_text,
                rating=rating,
                created_at=timezone.now()
            )

            image_path = image_gen(scenario_heading)
            scenario_feedback.image.save(os.path.basename(image_path), open(image_path, 'rb'))
            scenario_feedback.save()

            logger.info("---  Evaluated and genereated related image -----")
            # Return a JSON response
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    # Handle other HTTP methods or return an error for unsupported methods
    return JsonResponse({"error": "Unsupported HTTP method"}, status=405)


def journal(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Please login first.")
        return redirect('../login')

    user_object = UserProfile.objects.get(user=request.user.id)
    m_illness = random.choice(feelings)
    if user_object.illness != "":
        m_illness = user_object.illness

    quotes = quote_generation(m_illness)

    quotes_list = json.loads(quotes)
    final_list = quotes_list['quote']
    res = json.dumps(final_list)

    context = {
        'motivational_quotes': res
    }
    print(type(res))
    print(res)

    
    return render(request, 'journal.html', context)


def chatbot(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Please login first.")
        return redirect('../login')    

    
    logger.info("---  CHAT BUDDY setup -----")
    settings.MY_CHAT_BUDDY = bot_setup()

    user_object = UserProfile.objects.get(user=request.user.id)
    if user_object.moving_summary_buffer is not None:
        settings.MY_CHAT_BUDDY.memory.moving_summary_buffer = user_object.moving_summary_buffer
        settings.MY_CHAT_BUDDY.memory.chat_memory.messages = jsonpickle.loads(user_object.chat_memory_messages)

    if user_object.illness != "":
        settings.MY_CHAT_BUDDY.prompt.template = str(after_diagnosis_prompt+'the user is affected with'+user_object.illness)
        # print('------------CHAT BUDDY HERE-------------')
        # print(settings.MY_CHAT_BUDDY)
        # print('---------------------------')

    logger.info('---------moving_summary_buffer--------')
    logger.info(settings.MY_CHAT_BUDDY.memory.moving_summary_buffer)
    logger.info('---------chat_memory.messages--------')
    logger.info(settings.MY_CHAT_BUDDY.memory.chat_memory.messages)

    logger.info("---  CHAT BUDDY setup done -----")
    return render(request, 'chatbot.html',)

@csrf_exempt
def chatbot_qna(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Get the user's message from the JSON data
            user_message = data.get("usermessage", "")
            logger.info("--- user message -----")
            logger.info(user_message)
            # ans gets the answer response of particular function while calling quesry funtion
            
            
            # print("databse list here")
            # print(user_object.moving_summary_buffer)
            user_object = UserProfile.objects.get(user=request.user.id)

            # if user_object.illness == "":
            #    ans = settings.MY_CHAT_BUDDY(user_message)['response']
            # else:
            ans = settings.MY_CHAT_BUDDY(user_message)['response']    #UNCOMMENT THIS 
            # ans = " THIS IS BUDDY'S RESPOSNSE "
            # Prepare a response (e.g., chatbot response)
            response_data = {
                "message": ans,
            }

            # Return a JSON response
            
            # print(settings.MY_CHAT_BUDDY.memory.moving_summary_buffer)
            user_object.moving_summary_buffer = settings.MY_CHAT_BUDDY.memory.moving_summary_buffer
            new_list = jsonpickle.dumps(settings.MY_CHAT_BUDDY.memory.chat_memory.messages) 
            user_object.chat_memory_messages = new_list

            logger.info("--- adding to database ---")
            logger.info("---moving summay_buffer ---")
            logger.info(user_object.moving_summary_buffer)
            logger.info("--- chat_memory_messages ---")
            logger.info(settings.MY_CHAT_BUDDY.memory.chat_memory.messages)
            logger.info("-----------------------")
                
            
            user_object.save()
            # user_object.chat_memory_messages = user_object.set_message_list(new_list)
            

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    # Handle other HTTP methods or return an error for unsupported methods
    return JsonResponse({"error": "Unsupported HTTP method"}, status=405)

def diagnose(request):
    logger.info('-----mental illness here---')
    user_object = UserProfile.objects.get(user=request.user.id)
    if user_object.moving_summary_buffer != "":
        print(user_object.moving_summary_buffer)
        m_illness = analyze(user_object.moving_summary_buffer)
        user_object.illness = m_illness
        user_object.save()
    logger.info(m_illness)
    logger.info('-----mental illness diagnosed---')
    messages.info(request, "You are showing some symptoms related to " + str(m_illness))
    return redirect('../chatbot')



def activity(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Please login first.")
        return redirect('../login')
    return render(request, 'activity.html')

def articles(request):
    if not request.user.is_authenticated:
        # If the user is not authenticated, show a message and redirect to the login page
        messages.info(request, "Please login first.")
        return redirect('../login')
    user_object = UserProfile.objects.get(user=request.user.id)
    gender = user_object.gender
    status = user_object.relationship_status
    dob= user_object.date_of_birth
    age = calculate_age(dob)
    
    m_illness = random.choice(feelings)

    if user_object.illness != "":
        m_illness = user_object.illness

    # buddy = pp_generation("Internet Gaming Disorder", age, gender, status)
    
    

    # buddy_response = json.loads(buddy)

    # for goal_key, goal_data in buddy_response.items():
    #     print(goal_key)
    #     print(goal_data)
    #     article = Article.objects.create(
    #         user = request.user,
    #         title = goal_data['Text'],
    #         objective = goal_data['Objective'],
    #         timeframe = goal_data['Timeframe'],
    #         quote = goal_data['Motivation']
    #     )

    #     article.strategies = jsonpickle.dumps(goal_data['Strategies'])
    #     article.save()
    
    article_bool = Article.objects.filter(user=request.user.id)
    if len(article_bool) == 0:
            buddy = pp_generation(m_illness, age, gender, status)
            buddy_response = json.loads(buddy)
            print(buddy_response)
            for goal_key, goal_data in buddy_response.items():
                # print(goal_key)
                # print(goal_data)
                article = Article.objects.create(
                    user = request.user,
                    title = goal_data['Text'],
                    objective = goal_data['Objective'],
                    timeframe = goal_data['Timeframe'],
                    quote = goal_data['Motivation']
                )

                article.strategies = jsonpickle.dumps(goal_data['Strategies'])
                article.save() 

    first_4_articles = Article.objects.filter(user=request.user.id)[:4]

    new_buddy_response = {}
    count = 1
    for items in first_4_articles:
        article_data = {}
        article_data['Text'] = items.title
        article_data['Objective'] = items.objective
        article_data['Timeframe'] = items.timeframe
        article_data['Strategies'] = jsonpickle.loads(items.strategies)
        article_data['Motivation'] = items.quote

        new_buddy_response['Goal '+ str(count)] = article_data
        count = count + 1 

    context = {
        'buddy_response': new_buddy_response,
    }

    # print(m_illness)
    print("article gen here -----")
    print(new_buddy_response)

    return render(request, 'articles.html', context)



def fitness(request):
    fitness_data = get_today_activity_data()

    restructured_data = new_json()

    get_all_plans(restructured_data)
    # # health_goal = health_recommendation(restructured_data)
    # # exercise_goal = exercise_recommendation(restructured_data)

    context ={
        'fitness_data' : fitness_data
    }

    print(fitness_data)
    return render(request, 'watch copy.html', context)