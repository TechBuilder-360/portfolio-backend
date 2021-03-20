from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User


class UserDetailViewSet(APIView):
    """
    API endpoint that allows user detail to be viewed.
    """

    def get(self, request, id, format=None):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user)
            print(str(serializer.data))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            print("User with id %d not found" % id)
            return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
