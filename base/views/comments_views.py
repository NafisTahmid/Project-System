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
def getComment(request, pk):
    comment = Comments.objects.get(pk=pk)
    serializer = CommentsSerializer(comment, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateComment(request, pk):
    data = request.data
    comment = Comments.objects.get(pk=pk)
    comment.content = data.get('content', '')

    if 'user' in data:

        try:
            user = User.objects.get(pk=data['user'])
            comment.user = user
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=400)

    if 'task' in data:
        try:
            task = Tasks.objects.get(pk=data['task'])
            comment.task = task
        except Tasks.DoesNotExist:
            return Response({'error': 'Task not found'}, status=400)
   
    comment.save()
    serializer = CommentsSerializer(comment, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deleteComment(request, pk):
    comment = Comments.objects.get(pk=pk)
    comment.delete()
    message = "Comment deleted successfully"
    return Response(message, status=status.HTTP_200_OK)