from django.contrib.auth import get_user_model
from django.core.paginator import PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from django.contrib import messages

from .models import Post

User = get_user_model()


def post_list(request):
    posts = Post.objects.all()
    try:
        paginator = Paginator(posts, 2)
        page_number = int(request.GET.get("page"))
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        posts = paginator.page(1)
    context = {"posts": posts, "paginator": paginator}
    return render(request, "post/post_list.html", context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    return render(request, "post/post_detail.html", {"post": post})


def post_comment(request):
    if request.method != "POST":
        return render(
            request, "post/post_detail.html", {"error": "Invalid request method."}
        )
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    data = {"body": "Jude is a freak"}
