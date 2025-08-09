from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages 


def index(request):
    return render(request, 'mytasks1/index.html')

def archive(request):
    return render(request, 'mytasks1/archive.html')

def email(request):
    return render(request, 'mytasks1/email.html')
def data_log(request):
    return render(request, 'mytasks1/data_log.html')
def albums(request):
    return render(request, 'mytasks1/albums.html')
def notepad(request):
    return render(request, 'mytasks1/notepad.html')
def heart(request):
    return render(request, 'mytasks1/heart.html')

def send_email(request):
    if request.method == 'POST':
        try:
            subject = "Message from Your Site"
            message = "I miss you."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ["hanfeng.zhu@connect.polyu.hk"]
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            messages.success(request, "I have received your love.")
        except Exception as e:
            messages.error(request, f"Failed:{str(e)}")
        return redirect('email')
    return redirect('email')
    
def archive_email(request):
    # 这里可以添加获取Email分类数据的逻辑
    return render(request, 'mytasks1/archive_email.html')

def archive_photo(request):
    # 这里可以添加获取Photo分类数据的逻辑
    return render(request, 'mytasks1/archive_photo.html')

def archive_message(request):
    # 这里可以添加获取Message分类数据的逻辑
    return render(request, 'mytasks1/archive_message.html')

def archive_emotion(request):
    # 这里可以添加获取Emotion分类数据的逻辑
    return render(request, 'mytasks1/archive_emotion.html')

def archive_days(request):
    # 这里可以添加获取Days Matter分类数据的逻辑
    return render(request, 'mytasks1/archive_days.html')
