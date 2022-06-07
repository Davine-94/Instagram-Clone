from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Image, Profile, Likes, Comments, User
from django.db import models
import cloudinary
import cloudinary.uploader
import cloudinary.api


# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    '''
    get all the images from the database and order them by the date they were created
    '''
    images = Image.objects.all()
    return render(request, 'index.html', {'images': images})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    images = Image.objects.filter(user_id=current_user.id)
    profile = Profile.objects.filter(username_id=current_user.id).first()
    return render(request, 'profile.html', {"images": images, "profile": profile})


@login_required(login_url='/accounts/login/')
def like_image(request, id):
    likes = Likes.objects.filter(image_id=id).first()

    if Likes.objects.filter(image_id=id, user_id=request.user.id).exists():

        likes.delete()

        image = Image.objects.get(id=id)

        if image.total_likes == 0:
            image.total_likes = 0
            image.save()
        else:
            image.total_likes -= 1
            image.save()
        return redirect('/')
    else:
        likes = Likes(image_id=id, user_id=request.user.id)
        likes.save()
        image = Image.objects.get(id=id)
        image.total_likes = image.total_likes + 1
        image.save()
        return redirect('/')


@login_required(login_url='/accounts/login/')
def image_comments(request, id):
    image = Image.objects.get(id=id)

    related_images = Image.objects.filter(
        user_id=image.user_id)
    title = image.name

    if Image.objects.filter(id=id).exists():

        comments = Comments.objects.filter(image_id=id)
        return render(request, 'image_details.html', {'image': image, 'comments': comments, 'images': related_images, 'title': title})
    else:
        return redirect('/')


@login_required(login_url='/accounts/login/')
def save_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        image_id = request.POST['image_id']
        image = Image.objects.get(id=image_id)
        user = request.user
        comment = Comments(comment=comment, image_id=image_id, user_id=user.id)
        comment.save_comment()

        image.total_comments = image.total_comments + 1
        image.save()
        return redirect('/picture/' + str(image_id))
    else:
        return redirect('/')


@login_required(login_url='/accounts/login/')
def user_profile(request, id):

    if User.objects.filter(id=id).exists():

        user = User.objects.get(id=id)

        images = Image.objects.filter(user_id=id)

        profile = Profile.objects.filter(username_id=id).first()
        return render(request, 'user_profile.html', {'images': images, 'profile': profile, 'user': user})
    else:
        return redirect('/')


@login_required(login_url='/accounts/login/')
def search_images(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        images = Image.search_by_image_name(search_term)
        message = f'{search_term}'
        title = message

        return render(request, 'search.html', {'success': message, 'images': images})
    else:
        message = 'You havent searched for any term'
        return render(request, 'search.html', {'danger': message})


@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':

        current_user = request.user

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        bio = request.POST['bio']

        profile_image = request.FILES['profile_pic']
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image['url']

        user = User.objects.get(id=current_user.id)

        if Profile.objects.filter(username_id=current_user.id).exists():

            profile = Profile.objects.get(username_id=current_user.id)
            profile.photo = profile_url
            profile.bio = bio
            profile.save()
        else:
            profile = Profile(username_id=current_user.id,
                              photo=profile_url, bio=bio)
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect('/profile', {'success': 'Profile Updated Successfully'})

    else:
        return render(request, 'profile.html', {'danger': 'Profile Update Failed'})


@login_required(login_url='/accounts/login/')
def save_image(request):
    if request.method == 'POST':
        image_name = request.POST['image_name']
        image_caption = request.POST['image_caption']
        image_file = request.FILES['image_file']
        image_file = cloudinary.uploader.upload(image_file)
        image_url = image_file['url']
        image = Image(name=image_name, caption=image_caption, image=image_url,
                      profile_id=request.POST['user_id'], user_id=request.POST['user_id'])
        image.save_image()
        return redirect('/', {'success': 'Image Uploaded Successfully'})
    else:
        return render(request, 'profile.html', {'danger': 'Image Upload Failed'})
