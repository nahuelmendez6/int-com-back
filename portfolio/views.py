from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Portfolio, PortfolioAttachment
from .serializers import PortfolioSerializer, PortfolioAttachmentSerializer


class PortfolioAPIView(APIView):
    """
    GET: Lista todos los portfolios (o los del proveedor si se pasa id_provider)
    POST: Crea un nuevo portfolio
    """

    def get(self, request):
        id_provider = request.query_params.get('id_provider', None)
        if id_provider:
            portfolios = Portfolio.objects.filter(id_provider=id_provider)
        else:
            portfolios = Portfolio.objects.all()

        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            print(request.user.id_user)
            serializer.save(id_user_create=request.user.id_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioDetailAPIView(APIView):

    """
    GET: Obtiene un portfilio especifico por ID
    PATCH: Actualiza un portfolio
    """

    def get(self, request, id_portfolio):
        portfolio = get_object_or_404(Portfolio, id_portfolio=id_portfolio)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id_portfolio):
        portfolio = get_object_or_404(Portfolio, id_portfolio=id_portfolio)
        serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(id_user_update=request.user.id_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PortfolioAttachmentAPIView(APIView):
    """
    GET: Lista los adjuntos (puede filtrarse por id_portfolio)
    POST: Crea un nuevo adjunto (archivo)
    """

    def get(self, request):
        id_portfolio = request.query_params.get('id_portfolio', None)
        if id_portfolio:
            attachments = PortfolioAttachment.objects.filter(id_portfolio=id_portfolio)
        else:
            attachments = PortfolioAttachment.objects.all()

        serializer = PortfolioAttachmentSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PortfolioAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id_user_upload=request.user.id_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioAttachmentDetailAPIView(APIView):
    """
    GET: Obtiene un adjunto específico
    DELETE: Elimina un adjunto
    """

    def get(self, request, id_attachment):
        attachment = get_object_or_404(PortfolioAttachment, id_attachment=id_attachment)
        serializer = PortfolioAttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id_attachment):
        attachment = get_object_or_404(PortfolioAttachment, id_attachment=id_attachment)
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
