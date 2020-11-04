from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import exceptions
from .serializers import DocumentSerializer
from .models import Document


""" CRUD Operations on Documents

    Create Document by user

    Read Document owned by user

    Update Document owned by user

    Delete Document owned by user

    List of documents owned by user
"""
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_update_delete_document(request, slug):
    user_id = request.user['user_id']

    # search for document by slug
    try:
        document = Document.objects.get(user_id=user_id, slug=slug)
    except Document.DoesNotExist:
        raise exceptions.NotFound()
    serializer = DocumentSerializer(document)

    # Read
    if request.method == 'GET':
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    # Update
    elif request.method in ['PUT', 'PATCH']:
        request.data['user_id'] = user_id
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
        return Response(serializer.data)

    # Delete
    elif request.method == 'DELETE':
        document.delete()
        return Response({})


@api_view(['GET'])
def get_document(request, slug):
    """ Get a specific document (owned by user)
    """
    user_id = request.user['user_id']

    try:
        document = Document.objects.get(user_id=user_id, slug=slug)
    except Document.DoesNotExist:
        raise exceptions.NotFound()
    serializer = DocumentSerializer(document)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def update_document(request, slug):
    """ Update an existing document (owned by user)
    """
    user_id = request.user['user_id']
    request.data['user_id'] = user_id

    try:
        document = Document.objects.get(user_id=user_id, slug=slug)
    except Document.DoesNotExist:
        raise exceptions.NotFound()

    serializer = DocumentSerializer(document, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_document(request, slug):
    """ Delete an existing document (owned by user)
    """
    user_id = request.user['user_id']

    try:
        document = Document.objects.get(user_id=user_id, slug=slug)
    except Document.DoesNotExist:
        raise exceptions.NotFound()

    document.delete()
    return Response({})


@api_view(['GET', 'POST'])
def list_or_create_document(request):
    """ Get a list of existing documents (owned by user)
        or Create a new document
    """
    user_id = request.user['user_id']
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
