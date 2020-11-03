from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .serializers import DocumentSerializer


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
    if request.method == "GET":
        return Response({"action": "Get a list of existing documents"})

    elif request.method == "POST":
        return Response({"action": "Create a new document"})