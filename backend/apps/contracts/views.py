# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Contract
from .serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Contracts
    """

    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contract.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Optional: safer delete with ownership check
        """
        contract = get_object_or_404(Contract, id=kwargs["pk"], user=request.user)
        contract.delete()
        return Response(
            {"message": "Contract deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
