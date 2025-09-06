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
            subject = "极速版V8"
            message = """To Zhu,
今天邮件的发送方式非常先进,以至于我在发送之前给自己先发了一个testing版本。既然是极速版,那就不长篇大论了,引用一下我今天日记里的话吧:
我们不能要求任何人是完美的，也不能要求任何爱是完美的。最重要的是，是否愿意为了那个“不可能的完美”，做出一点改变和牺牲。
圆圆已经在努力了，请留给我些许耐心。
晚安,
爱你的小圆
2025.8.12 22:18"""
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ["zhuhanfng066@qq.com"]
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
