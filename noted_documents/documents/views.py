from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import exceptions
from .serializers import DocumentSerializer
from .models import Document


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_update_delete_document(request, slug):
    """ Read-Update-Delete operations on single documents

        Depending on the method used, this view will execute
        a different task
    """
    user_id = request.user.id

    # search for document by slug
    try:
        document = Document.objects.get(user_id=user_id, slug=slug)
    except Document.DoesNotExist:
        raise exceptions.NotFound()
    serializer = DocumentSerializer(document)

    # Read document
    if request.method == 'GET':
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    # Update document
    elif request.method in ['PUT', 'PATCH']:
        request.data['user_id'] = user_id
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        return Response(serializer.data)

    # Delete document
    elif request.method == 'DELETE':
        document.delete()
        return Response({})


@api_view(['GET', 'POST'])
def list_or_create_document(request):
    """ Get a list of existing documents (owned by user)
        or Create a new document
    """
    user_id = request.user.id
    request.data['user_id'] = user_id

    # Return a list of Documents owned by the user making the request
    if request.method == "GET":
        # TODO: add pagination
        queryset = Document.objects.filter(user_id=user_id)
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)

    # Create a new document
    elif request.method == "POST":
        instance = None
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # instance = serializer.create(serializer.validated_data)
            instance = serializer.save()
        
        print(instance)
        return Response(serializer.data)
