from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import ApplicationSerializer
from .models import Application
from rest_framework import status


class ApplicationView(APIView):
    def get(self, request, id=None):
        if id:
            # Handle GET request for a specific application by ID
            try:
                application = Application.objects.get(id=id)
                serializer = ApplicationSerializer(application)
                return Response(serializer.data)
            except Application.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Application not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            # Handle GET request to retrieve the latest application data
            latest_application = Application.objects.order_by("-id").first()
            if latest_application:
                serializer = ApplicationSerializer(latest_application)
                return Response(serializer.data)
            else:
                return Response({"status": "error", "message": "No applications found"})

    def post(self, request, *args, **kwargs):
        # Handle POST request to create a new application
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            return Response({"status": "success", "id": application.id})
        else:
            return Response({"status": "error", "errors": serializer.errors})
