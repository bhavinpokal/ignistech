from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer, EventSerializer
from .models import Event


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            refresh = RefreshToken.for_user(serializer.instance)
            return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        # if user:
        #     token = user.get_jwt_token()
        #     response = Response({'token': token}, status=status.HTTP_200_OK)
        #     response.set_cookie(key='jwt', value=token, httponly=True)
        #     return response
        # else:
        #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateEventAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(created_by=request.user)

            # Save image file
            image = request.FILES.get('image')
            if image:
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                event.image = fs.url(filename)
                event.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllEventListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class UserEventListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        events = Event.objects.filter(created_by=request.user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        user = request.user

        if user in event.likes.all():
            event.likes.remove(user)
            return Response({'liked': False}, status=status.HTTP_200_OK)
        else:
            event.likes.add(user)
            return Response({'liked': True}, status=status.HTTP_200_OK)
