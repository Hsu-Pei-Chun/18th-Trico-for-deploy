from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm
from .models import Category
from comments.models import Comment
from comments.forms import CommentForm
from django.db import models
import json


def has_permission(request, id):
    return request.user.id == id


@login_required
def freelancer_dashboard(request, id):

    if not has_permission(request, id):
        return redirect("services:error_page")

    freelancer = request.user

    services = (
        Service.objects.prefetch_related("category")
        .filter(freelancer_user=freelancer)
        .order_by("-created_at")
    )

    return render(
        request,
        "services/freelancer_dashboard.html",
        {
            "freelancer": freelancer,
            "services": services,
        },
    )


@login_required
def create_service(request, id):
    if not has_permission(request, id):
        return redirect("services:error_page")

    categories = Category.objects.all()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.freelancer_user = request.user
            service.save()
            selected_categories = request.POST.getlist("category")
            service.category.set(selected_categories)
            return redirect("services:freelancer_dashboard", id=id)
    else:
        form = ServiceForm()

    return render(
        request,
        "services/create_service.html",
        {"form": form, "categories": categories},
    )



@login_required
def edit_service(request, id, service_id):
    if not has_permission(request, id):
        return redirect("services:error_page")

    service = get_object_or_404(Service, id=service_id, freelancer_user=request.user)
    categories = Category.objects.all()

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            selected_categories = request.POST.getlist("category")
            service.category.set(selected_categories)
            return redirect("services:freelancer_dashboard", id=id)
    else:
        form = ServiceForm(instance=service)

    return render(
        request,
        "services/edit_service.html",
        {"form": form, "categories": categories},
    )



@login_required
def delete_service(request, id, service_id):
    if not has_permission(request, id):
        return redirect("services:error_page")

    service = get_object_or_404(Service, id=service_id, freelancer_user=request.user)

    if request.method == "POST":
        service.delete()
        return redirect("services:freelancer_dashboard", id=id)

    return render(
        request, "services/delete_service.html", {"service": service, "id": id}
    )


def error_page(request):
    return render(
        request,
        "services/error_page.html",
        {"message": "You do not have permission to view this page."},
    )



@login_required
def service_detail(request, id, service_id):
    service = get_object_or_404(Service, id=service_id)
    comments = Comment.objects.filter(service=service, is_deleted=False).order_by(
        "-created_at"
    )

    total_reviews = comments.count()

    average_rating = comments.aggregate(models.Avg("rating"))["rating__avg"]

    grouped_ratings = comments.values("rating").annotate(count=models.Count("rating"))
    stars_count = {i: 0 for i in range(1, 6)}

    for group in grouped_ratings:
        stars_count[group["rating"]] = group["count"]
    
    try:
        comment = Comment.objects.get(service=service, user=request.user)
    except Comment.DoesNotExist:
        comment = None
    
    form = CommentForm(request.POST or None ,instance=comment)

    if request.method == "POST":
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.service = service
            comment.rating = request.POST.get("rating")
            comment.is_deleted = False
            comment.deleted_at = None
            comment.save()
            return redirect(
                "services:service_detail", id=request.user.id, service_id=service_id
            )
        
    if comment and comment.is_deleted:
        comment = None
        form = CommentForm()

    return render(
        request,
        "services/service_detail.html",
        {
            "service": service,
            "comments": comments,
            "comment": comment,
            "form": form,
            "stars_count": stars_count,
            "total_reviews": total_reviews,
            "average_rating": average_rating,
        },
    )
