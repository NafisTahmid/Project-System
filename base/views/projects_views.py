from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import ProjectsSerializer, TaskSerializer
from base.models import Projects, Tasks
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
@api_view(['GET'])
def listProjects(request):
    projects = Projects.objects.all()
    serializer = ProjectsSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Projects.objects.get(pk=pk)
    serializer = ProjectsSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProject(request):
    data = request.data
    user = request.user
    project_owner = User.objects.get(pk=user.pk)
    project = Projects.objects.create(
        name = data.get('name', ''),
        description = data.get('description', ''),
        owner = project_owner
    )
    project.save()
    serializer = ProjectsSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProject(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    data = request.data
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.save()

    serializer  = ProjectsSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProject(request, pk):
    project = Projects.objects.get(pk=pk)
    project.delete()
    message = "Project deleted successfully"
    return Response(message, status=status.HTTP_202_ACCEPTED)
    
@api_view(['GET'])
def listTasks(request, pk):
    project = Projects.objects.get(pk=pk)
    tasks = Tasks.objects.filter(project=project)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createTask(request, pk):
    try:
        project = Projects.objects.get(pk=pk)
    except Projects.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    
    data = request.data

    assigned_to = None
    if 'assigned_to' in data:
        try:
            assigned_to = User.objects.get(id=data['assigned_to']) 
        except User.DoesNotExist:
            return Response({'error': 'Assigned user not found'}, status=404)
        
    task = Tasks.objects.create(
        title = data.get('title', ''), 
        description = data.get('description', ''), 
        status = data.get('status', 'To Do'), 
        priority = data.get('priority', 'Medium'),
        project = project, 
        assigned_to = assigned_to  
    )
    
    task.save()
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

