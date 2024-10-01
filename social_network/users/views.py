from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import FriendRequest
from .serializers import FriendSerializer
from .serializers import PendingFriendRequestSerializer
from .models import UserActivity 
from .serializers import UserActivitySerializer 

User = get_user_model()

class UserSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({"message": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST)

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    

class UserSearchView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination
    serializer_class = UserSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('search', None)
        if keyword:
            return User.objects.filter(
                Q(email__iexact=keyword) |
                Q(email__icontains=keyword) |
                Q(first_name__icontains=keyword) |
                Q(last_name__icontains=keyword)
            )
        return User.objects.none()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No users found matching the search keyword."}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, receiver_id):
        try:
            receiver = User.objects.get(id=receiver_id)
            if receiver == request.user:
                return Response({"message": "You cannot send a friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

            existing_request = FriendRequest.objects.filter(sender=request.user, receiver=receiver).first()
            if existing_request:
                return Response({"message": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the friend request
            friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver)

            # Log the activity
            UserActivity.objects.create(user=request.user, activity_type="friend_request_sent", details=f"Sent to {receiver.email}")

            return Response({"message": "Friend request sent successfully"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class RespondToFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id, action):
        try:
            friend_request = FriendRequest.objects.get(id=request_id)

            if friend_request.receiver != request.user:
                return Response({"message": "You are not authorized to respond to this friend request."}, status=status.HTTP_403_FORBIDDEN)

            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()

                # Log the activity
                UserActivity.objects.create(user=request.user, activity_type="friend_request_accepted", details=f"Accepted from {friend_request.sender.email}")

                return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)

            elif action == 'reject':
                friend_request.status = 'rejected'
                friend_request.save()

                # Log the activity
                UserActivity.objects.create(user=request.user, activity_type="friend_request_rejected", details=f"Rejected from {friend_request.sender.email}")

                return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)

            return Response({"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        except FriendRequest.DoesNotExist:
            return Response({"message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)


class UserActivityView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivitySerializer
    pagination_class = UserPagination

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user).order_by('-timestamp')


class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the accepted friend requests where the current user is either sender or receiver
        accepted_requests_as_sender = FriendRequest.objects.filter(sender=request.user, status='accepted')
        accepted_requests_as_receiver = FriendRequest.objects.filter(receiver=request.user, status='accepted')

        # Extract the friends' user objects
        friends_as_sender = [req.receiver for req in accepted_requests_as_sender]
        friends_as_receiver = [req.sender for req in accepted_requests_as_receiver]

        # Combine friends lists
        friends = friends_as_sender + friends_as_receiver

        # Serialize the user data
        serializer = FriendSerializer(friends, many=True)

        return Response(serializer.data, status=200)


class PendingFriendRequestPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PendingFriendRequestsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PendingFriendRequestSerializer
    pagination_class = PendingFriendRequestPagination

    def get_queryset(self):
        # Fetch pending friend requests for the logged-in user
        queryset = FriendRequest.objects.filter(receiver=self.request.user, status='pending')
        
        # Get the sorting parameter from the query parameters
        sort_by = self.request.query_params.get('sort', '-created_at')  # Default is descending by 'created_at'
        
        # Return the queryset ordered by the specified field
        return queryset.order_by(sort_by)