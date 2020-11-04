from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .serializers import DocumentSerializer
from .models import Document


""" CRUD Operations on Documents

    Create Document by user

    Read Document owned by user

    Update Document owned by user

    Delete Document owned by user

    List of documents owned by user
"""


@api_view(['GET'])
def get_document(request, slug):
    """ Get a specific document (owned by user)
    """
    # print(request.virtual_user_id)
    return Response({"action": "get a specific document, {slug}".format(slug=slug)})


@api_view(['PUT', 'PATCH'])
def update_document(request, slug):
    """ Update an existing document (owned by user)
    """
    return Response({"action": "update an existing document, {slug}".format(slug=slug)})


@api_view(['DELETE'])
def delete_document(request, slug):
    """ Delete an existing document (owned by user)
    """
    return Response({"action": "delete an existing document, {slug}".format(slug=slug)})


@api_view(['GET', 'POST'])
def list_or_create_document(request):
    """ Get a list of existing documents (owned by user)
        or Create a new document
    """
    user_id = request.user['user_id']
    request.data['user_id'] = user_id

    # Return a list of Documents owned by the user making the request
    if request.method == "GET":
        queryset = Document.objects.filter(user_id=user_id)
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)

    # Create a new document
    elif request.method == "POST":
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
        
        return Response({"action": "Create a new document"})
