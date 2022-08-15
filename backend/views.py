from django.http import HttpResponse
from django.shortcuts import redirect, render
from  django.contrib import messages
from backend.models import bookmarked_files, file_likes, file_upload, reported_file, user_details
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import random
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

def home(request):
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")

    user_is_admin = False
    name = "User"
    if username != None:
        user_detail = user_details.objects.get(Q(pk = user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name 
        
        
    context = {
        'current_user': user_id,
        'username': username,
        'is_admin': user_is_admin,
        'name':name
    }
    return render(request,'pages/home/index.html',context)


def profile(request):
    return render(request,'pages/profile/user_profile.html')






def loginpage(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            validate_userid = user_details.objects.get(Q(username = username),Q(password = password))
            user_unique_id = validate_userid.pk
            user_is_active = validate_userid['is_active']
            request.session['user_unique_id'] = user_unique_id
            request.session['username'] = username
            context={
                    'username':username,
                    'user_unique_id':user_unique_id
                    }
            if(user_is_active):
                return redirect("/",args=context)
            else:
                return redirect("/otp_page")
        except:
            messages.error(request,"Invalid credentials")

    return render(request,'pages/login_page/login_page.html')








# def registration(request):
#     return render(request,'pages/loginandsignup/reg_page.html')


def about(request):
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    user_is_admin = ''
    name = ''
    if username != None:
        user_detail = user_details.objects.get(Q(pk = user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name 
        

    context = {
        'current_user': user_id,
        'username': username,
        'user_is_admin':user_is_admin,      
        'name':name,
    }   
    return render(request,'pages/other/about/aboutus.html',context)

def contact(request):
    user_id = request.session.get("user_unique_id")
    context = {
        'current_user': user_id
    }
    return render(request,'pages/other/contact/contact.html',context)




# login & signup backend
def signuppage(request):

    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        gender = request.POST['gender'] 
        dob = request.POST['dob']
        mail = request.POST['mail'] 
        phone = request.POST['phone'] 
        username = request.POST['username'] 
        password = request.POST['password'] 
        print(username)

        exists_username = user_details.objects.filter(username = username).count()
        exists_email = user_details.objects.filter(mail = mail).count()

        if exists_username > 0:
            print("username error")
            messages.error(request,"Username Exist")
            
        elif exists_email > 0:
            print("email error")
            messages.error(request,"Email Exist")
        else:
            users = user_details.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender = gender,
                dob = dob,
                mail = mail,
                phone = phone,
                username = username,
                password = password,
                )
            users.save()
            print("User Created")
            # We will load the html content first
            random_num = random.randint(1000,9999)

            html_content = render_to_string("pages/other/mail_template/emailtemplate.html", {'name': first_name ,'otp':random_num })

            # html content jo load karenge usme se HTML tags nikal denge
            text_content = strip_tags(html_content)
            mail = EmailMultiAlternatives(  # Initialize a single email message (which can be sent to multiple recipients).
                # subject
                "Please Verify Your Account",
                # content
                text_content,
                # from email
                'findmynotes2002@gmail.com',
                # receipient list
                [mail]
            )

            # attach the html content
            mail.attach_alternative(html_content, "text/html")
            mail.send()
            request.session["new_user"] = username
            request.session["new_user_id"] = users.unique_id
            request.session["new_otp"] = random_num 
            return redirect(otp_page)

    return render(request,'pages/reg_page/reg_page.html')


def otp_page(request):
    if request.method == "POST":
        input_otp = request.POST['otp_input']
        if input_otp == str(request.session.get('new_otp')):
            set_active = user_details.objects.get(username = request.session.get("new_user"))
            set_active.is_active = True
            set_active.save()
            request.session['username'] = request.session.get("new_user")
            request.session['user_unique_id'] = request.session.get("new_user_id")
            return redirect(home)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,"pages/other/otp/otp_page.html")


def searchPage(request,category='',query=''):

    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")

    name = ''
    if username != None:
        user_detail = user_details.objects.get(Q(pk = user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name 

    context= {}
    context['current_user'] = user_id
    context['username'] = username
    context['user_is_admin'] = user_is_admin
    context['name'] = name
    

    if category != '' and query != '':
        
        search_query = query

        print(search_query)

        resources = file_upload.objects.filter(Q(description = search_query) | Q(file_title = search_query))
        liked_resources = file_likes.objects.filter(Q(user = user_id),Q(file__in = resources))

        # creating list of liked files in search result bu user
        liked_by_user = []
        for dataset in liked_resources:
            if dataset.pk not in liked_by_user:
                liked_by_user.append(dataset.file.pk)


        bookmarked_resources = bookmarked_files.objects.filter(Q(user = user_id),Q(file__in = resources))

        # creating list of bookmarked files in search result bu user
        bookmarked_by_user = []
        for dataset in bookmarked_resources:
            if dataset.pk not in bookmarked_by_user:
                bookmarked_by_user.append(dataset.file.pk)

        print(resources)
        
        context['all_resources'] = resources
        context['liked_by_user'] = liked_by_user
        context['bookmarked_by_user'] = bookmarked_by_user
        context['user_is_admin'] = user_is_admin
        context['name'] = name

        
        # print("--",context['resources'])
    return render(request,"pages/search/search_page.html",context)



def file_like(request):

    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            print(request.GET.get('file_id',None))
            file_id = request.GET.get('file_id',None)
            # print("File_id: ",file_id)
            create_file_like_object = file_likes.objects.create(
                user = user_details.objects.get(unique_id = user_id),
                file = file_upload.objects.get(pk = file_id)
            )
            create_file_like_object.save()

            like_count = count_likes(file_id)

            # print("count: ",count_likes(file_id))

            return HttpResponse('Success,'+str(like_count))

        except Exception as er:
            return HttpResponse("Error: "+str(er))


def file_unlike(request):
    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            file_id = request.GET.get('file_id',None)

            get_file_like_object = file_likes.objects.get(Q(file = file_id), Q(user = user_id))
            get_file_like_object.delete()
            
            like_count = count_likes(file_id)

            return HttpResponse('Success,'+str(like_count))

        except Exception as er:
            return HttpResponse("Error: "+str(er))


def count_likes(file_id):
    get_like_db_count = file_likes.objects.filter(Q(file = file_id)).count() 
    file_db_update = file_upload.objects.get(pk = file_id)
    file_db_update.likes = int(get_like_db_count)
    file_db_update.save()
    return get_like_db_count
    


def add_bookmark(request):

    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            print(request.GET.get('file_id',None))
            file_id = request.GET.get('file_id',None)
            # print("File_id: ",file_id)
            create_bookmark_file_object = bookmarked_files.objects.create(
                user = user_details.objects.get(unique_id = user_id),
                file = file_upload.objects.get(pk = file_id)
            )
            create_bookmark_file_object.save()

            # print("count: ",count_likes(file_id))

            return HttpResponse("Success")
        except Exception as er:
            return HttpResponse("Error: "+str(er))


def remove_bookmark(request):
    user_id = request.session.get("user_unique_id")
    if request.method == "POST":
        try:
            file_id = request.GET.get('file_id',None)

            bookmark_file_object = bookmarked_files.objects.get(Q(file = file_id), Q(user = user_id))
            bookmark_file_object.delete()
            
            return HttpResponse("Success")
        except Exception as er:
            return HttpResponse("Error: "+str(er))


def report_submit(request):
    if request.method == "POST":
        try:

            file_id = request.GET.get('file_id',None)
            user_reported_issue = request.GET.get('user_reported_issue',None)
            user_posted = request.GET.get('user_posted',None)
            report_topic = request.GET.get('report_topic',None)
            reason_to_report = request.GET.get('reason_to_report',None)
            
            file_id = file_upload.objects.get( Q(pk = file_id) )
            user_reported_issue= user_details.objects.get( Q(pk = user_reported_issue) )
            user_posted =  user_details.objects.get( Q(pk = user_posted) )

            print("->",file_id, user_reported_issue, user_posted)

            report_file_objects = reported_file.objects.create(
                file= file_id, 
                user_reported_issue = user_reported_issue,
                user_posted = user_posted,
                reason = report_topic,
                reason_message = reason_to_report,
                )
            report_file_objects.save()
            return HttpResponse("Success")

        except Exception as er:
            print("Error: "+str(er))
            return HttpResponse("Error: "+str(er))




def upload_page(request):
    
    user_id = request.session.get("user_unique_id")
    username = request.session.get("username")
    
    if username != None:
        user_detail = user_details.objects.get(Q(pk = user_id))
        user_is_admin = user_detail.is_admin
        name = user_detail.first_name 
        

    if request.method == "POST":

        file = request.FILES['file_data']
        file_type = request.POST['file_type']
        file_description = request.POST['description']
        file_title = request.POST['title']
        tags = request.POST['tags']
        fs = FileSystemStorage(location= 'files/'+str(request.session['user_unique_id'])+"/"+file_type+"/")
        file_details = file_upload.objects.create(
            file_type = file_type , 
            file_name = file.name,
            description = file_description,
            file_title = file_title,
            tags = tags,
            file_url = str(request.session['user_unique_id'])+"/"+file_type+"/"+file.name,
            user = user_details.objects.get(unique_id = request.session.get("user_unique_id")),
            likes = 0
            )
        file_details.save()
        fs.save(file.name,file)


    context = {
        'current_user': user_id,
        'username': username,
        'user_is_admin':user_is_admin,
        'name':name
    }
    return render(request,"pages/upload/old_upload.html",context)





def logout(request):
    request.session.flush()
    return redirect(loginpage)