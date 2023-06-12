from pathlib import Path
import os
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects


def projects(request):

    projects, search_query = searchProjects(request)
    
    custom_range, projects = paginateProjects(request,projects,4)

    context = {'projects': projects, 'search_query':search_query, 'custom_range':custom_range}

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        projectObj.getVoteCount # use getVoteCount property that we add it in the model to get and set the total votes and ratio
        messages.success(request,'Review was added successfully!')
        return redirect('project', pk)

    return render(request, 'projects/single-project.html', {'project': projectObj, 'form':form})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request,'Project was created successfully!')
            return redirect('user-account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request,'Project was deleted successfully!')
            return redirect('user-account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request,'Project was deleted successfully!')
        return redirect('user-account')
    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)
