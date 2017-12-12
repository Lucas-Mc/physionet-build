from django.contrib import messages
from django import forms
from django.forms import modelformset_factory
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os

from .forms import ProjectCreationForm
from .models import metadata_models, Project, DatabaseMetadata, SoftwareMetadata
from .utility import get_display_file, get_display_directory
from physionet.settings import STATIC_ROOT

import pdb
from user.forms import ProfileForm


def download_file(request, file_path):
    """
    Serve a file to download. file_path is the full file path of the file on the server
    """
    if os.path.exists(filepath):
        with open(filepath, 'r') as fh:
            response = HttpResponse(fh.read())
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    else:
        return Http404()

@login_required
def project_home(request):
    "Home page listing projects a user is involved in"
    
    user = request.user
    projects = Project.objects.filter(collaborators__in=[user])

    # Projects that the user is responsible for reviewing
    review_projects = None
    return render(request, 'project/project_home.html', {'projects':projects,
        'review_projects':review_projects})


@login_required
def create_project(request):
    user = request.user
    form = ProjectCreationForm(initial={'owner':user})

    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            print('\n\nvalid!')
            project = form.save(owner=user)

            return redirect('project_overview', project_id=project.id)

    return render(request, 'project/create_project.html', {'form':form})


@login_required
def project_overview(request, project_id):
    "Overview page of a project"
    user = request.user

    # Only allow access if the user is a collaborator
    # Turn this into a decorator, with login decorator
    project = Project.objects.get(id=project_id)
    collaborators = project.collaborators.all()
    if user not in collaborators:
        raise Http404("Unable to access project")

    return render(request, 'project/project_overview.html', {'project':project})


@login_required
def project_metadata(request, project_id):
    project = Project.objects.get(id=project_id)

    # Dynamically generate the metadata modelform for the relevant type
    #MetadataFormset = modelformset_factory(metadata_models[project.resource_type.description],
    MetadataFormset = modelformset_factory(DatabaseMetadata,
        exclude=('slug', 'id'))

    form = MetadataFormset(queryset=DatabaseMetadata.objects.filter(id=project.metadata.id))[0]

    if request.method == 'POST':
        
        formset = MetadataFormset(request.POST)

        # formset = AssociatedEmailFormset(request.POST, instance=user)
        #     set_public_emails(request, formset)

        if formset.is_valid():
            formset.save()
            messages.success(request, 'Your project metadata has been updated.')

    return render(request, 'project/project_metadata.html', {'project':project,
        'form':form, 'messages':messages.get_messages(request)})


@login_required
def project_files(request, project_id, sub_link=''):
    "View and manipulate files in a project"
    project = Project.objects.get(id=project_id)

    # Directory where files are kept for the project
    project_file_dir = os.path.join(STATIC_ROOT, project_id)

    # Case of accessing a file or subdirectory
    if sub_link:
        item_path = os.path.join(project_file_dir, sub_link)
        


        return download_file(request)


    file_names = sorted([f for f in os.listdir(project_file_dir) if os.path.isfile(os.path.join(project_file_dir, f)) and not f.endswith('~')])
    dir_names = sorted([d for d in os.listdir(project_file_dir) if os.path.isdir(os.path.join(project_file_dir, d))])

    display_files = [get_display_file(os.path.join(project_file_dir, f)) for f in file_names]
    display_dirs = [get_display_directory(os.path.join(project_file_dir, d)) for d in dir_names]

    return render(request, 'project/project_files.html', {'project':project,
        'display_files':display_files, 'display_dirs':display_dirs})


@login_required
def project_collaborators(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'project/project_collaborators.html', {'project':project})

