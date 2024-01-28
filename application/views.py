from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ApplicationSerializer

@api_view(['POST'])
def create_application(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        application = serializer.save()
        return Response({'status': 'success', 'id': application.id})
    else:
        return Response({'status': 'error', 'errors': serializer.errors})
    