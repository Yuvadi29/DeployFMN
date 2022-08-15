from email.policy import HTTP

from backend.models import bookmarked_files, file_likes, file_upload, reported_file, user_details
from django.shortcuts import redirect, render
from django.db.models import Q



# admin pages where he can approve and decline uploaded contents   
def adminfeed(request):

    users = user_details.objects.all().exclude(Q(is_active = False) and Q(is_admin = True))
    user_count = users.count()

    uploads = file_upload.objects.all()
    upload_count = uploads.count()

    reports = reported_file.objects.all()
    report_count = reports.count()

    bookmarked = bookmarked_files.objects.all()
    bookmarked_count = bookmarked.count()

    likes = file_likes.objects.all()
    likes_count = likes.count()

    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    if username != None:
        user_detail = user_details.objects.get(Q(pk = user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name

    context = {
        'current_user': user_id,
        'user_count':user_count,
        'report_count':report_count,
        'file_count':upload_count,
        'list_of_users':users,
        'list_of_reports':reports,
        'list_of_uploads':uploads,
        'username':username,
        'name':name,
    }
    return render(request,'pages/Admin/admin_panel.html',context)

def changeRole(request):
    user_id = request.GET['user_id']
    role = request.GET['role']

    print("User: ",user_id)
    print("role: ",role)

    user_data = user_details.objects.get(Q(pk = user_id)) 
    if role == "Admin":

        user_data.is_content_writer = 0
        user_data.is_faculty = 0
        user_data.is_student = 0
        user_data.is_admin = 1

    elif role == "Student":

        user_data.is_student = 1
        user_data.is_content_writer = 0
        user_data.is_faculty = 0
        user_data.is_admin = 0

    elif role == "Faculty":

        user_data.is_faculty = 1
        user_data.is_content_writer = 0
        user_data.is_student = 0
        user_data.is_admin = 0
    
    elif role == "Content Writer":  

        user_data.is_content_writer = 1
        user_data.is_faculty = 0
        user_data.is_student = 0
        user_data.is_admin = 0

    user_data.save()
    return redirect(adminfeed)


def admin_user_reports(request):    
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    if username != None:
        user_detail = user_details.objects.get(Q(pk = user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name 

    context = {
        'current_user': user_id,
        'username':username,
        'name':name
    }
    return render(request,'pages/Admin/user_reports.html',context)
