from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import TagManager,Admin,Annotators
import os
from django.conf import settings
from django.http import JsonResponse

@login_required(login_url='')
def home(request):
    tag_manager = TagManager.get_instance()
    return render(request, 'tags/home.html', {'tags': tag_manager.tags})

@csrf_exempt
def add_tag(request):
    if request.method == 'POST':
        tag_manager = TagManager.get_instance()
        data = json.loads(request.body)
        new_tag = data.get('tag')
        if new_tag and new_tag not in tag_manager.tags:
            tag_manager.tags.append(new_tag)
            tag_manager.save()
            return JsonResponse({'status': 'success', 'tags': tag_manager.tags})
    return JsonResponse({'status': 'error'})
# Create your views here.

@csrf_exempt
def clear_tags(request):
    if request.method == 'POST':
        try:
            # Get or create the TagManager instance
            tag_manager = TagManager.get_instance()
            
            # Clear the tags
            tag_manager.tags = []
            tag_manager.save()

            return JsonResponse({'status': 'success', 'message': 'All tags removed successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def submit_file(request):
    if request.method == 'POST':
        # Parse the filename from the POST request
        body = json.loads(request.body)
        filename = body.get('filename')

        if not filename:
            return JsonResponse({"status": "error", "message": "Filename is required."})

        # Path to the picked files JSON
        picked_files_path = os.path.join(settings.BASE_DIR, 'tagproject', 'picked_files.json')

        # Ensure the JSON file exists
        if not os.path.exists(picked_files_path):
            with open(picked_files_path, 'w') as f:
                json.dump([], f)

        # Load the picked files list
        with open(picked_files_path, 'r') as f:
            picked_files = json.load(f)

        # Add the filename if not already present
        if filename not in picked_files:
            picked_files.append(filename)
            with open(picked_files_path, 'w') as f:
                json.dump(picked_files, f)

        return JsonResponse({"status": "success", "message": f"File '{filename}' has been submitted."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})

def get_paragraph(request):
    # Define the path to the text files directory
    text_files_dir = os.path.join(settings.BASE_DIR, 'tagproject', 'text_files')
    
    # Define the path for the JSON file to track picked files
    picked_files_path = os.path.join(settings.BASE_DIR, 'tagproject', 'picked_files.json')

    # If the JSON file doesn't exist, create it with an empty list
    if not os.path.exists(picked_files_path):
        with open(picked_files_path, 'w') as f:
            json.dump([], f)

    # Load the list of picked files
    with open(picked_files_path, 'r') as f:
        picked_files = json.load(f)

    # List all text files in the directory
    all_text_files = [f for f in os.listdir(text_files_dir) if f.endswith('.txt')]

    # Find the remaining files that have not been picked yet
    remaining_files = [f for f in all_text_files if f not in picked_files]

    # Handle case when there are no remaining files
    if not remaining_files:
        return JsonResponse({"status": "error", "message": "All text files have been picked."})

    # Pick the next file (no sorting, just the first unpicked file in the list)
    next_file = remaining_files[0]
    file_path = os.path.join(text_files_dir, next_file)

    # Read the content of the picked file
    with open(file_path, 'r') as file:
        content = file.read()

    # Add the picked file to the list and update the JSON file
    # picked_files.append(next_file)
    # with open(picked_files_path, 'w') as f:
    #     json.dump(picked_files, f)

    return JsonResponse({"status": "success", "paragraph": content, "filename": next_file})

def reset_picked_files(request):
    picked_files_path = os.path.join(settings.BASE_DIR, 'tagproject', 'picked_files.json')

    try:
        print(f"Attempting to reset the file at {picked_files_path}")  # Debugging line
        with open(picked_files_path, 'w') as f:
            json.dump([], f)

        return JsonResponse({"status": "success", "message": "Picked files list has been reset."})
    
    except Exception as e:
        print(f"Error resetting picked files: {str(e)}")  # Debugging line
        return JsonResponse({"status": "error", "message": str(e)})

def login_page(request):
    
    if request.method == "POST":
        # admin_user = Admin.objects.create(username="admin", password="admin")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # Check for admin login
        try:
            admin_user = Admin.objects.get(username=username, password=password)
            if admin_user and user is not None:
                print("Admin authenticated")
                login(request,user)
                return redirect('/home')  # Redirect to admin home
            else:
                return render(request, 'registration/login.html')

        except Admin.DoesNotExist:
            pass  # Proceed to user login check if not admin

        # Check for annotator login
        try:
            annotator_user = Annotators.objects.get(username=username, password=password)
            if annotator_user and user is not None:
                print("Annotator authenticated")
                login(request,user)
                return redirect('/home')  # Redirect to user home
            else:
                return render(request, 'registration/login.html')
        except Annotators.DoesNotExist:
            pass

        # If neither admin nor user credentials match
        err_msg = {"msg": "Username or password is wrong, please try again"}
        return render(request, 'registration/login.html', err_msg)

    return render(request, 'registration/login.html')
        
