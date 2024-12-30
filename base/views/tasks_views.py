from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import TaskSerializer, CommentsSerializer
from base.models import Projects, Tasks, Comments
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def getTask(request, pk):
    task = Tasks.objects.get(pk=pk)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateTask(request, pk):
    data = request.data
    
    task = get_object_or_404(Tasks, pk=pk)
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    

    if 'assigned_to' in data:
        try:
            assigned_user = User.objects.get(pk=data['assigned_to'])
            task.assigned_to = assigned_user
        except User.DoesNotExist:
            return Response({'error': 'Assigned user not found'}, status=400)

    if 'project' in data:
        try:
            project = Projects.objects.get(pk=data['project'])
            task.project = project
        except Projects.DoesNotExist:
            return Response({'error': 'Project not found'}, status=400)
    
    task.save()
    
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteTask(request, pk):
    task = Tasks.objects.get(pk=pk)
    task.delete()
    message = "Task deleted successfully"
    return Response(message, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def getComments(request, pk):
    task = Tasks.objects.get(pk=pk)
    comments = Comments.objects.filter(task=task)
    serializer = CommentsSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createComment(request, pk):
    task = Tasks.objects.get(pk=pk)
    data = request.data
    user= request.user
    comment = Comments.objects.create(
        content = data['content'],
        user = user,                              
        task = task   
    )
    serializer = CommentsSerializer(comment, many=False)
    return Response(serializer.data)

