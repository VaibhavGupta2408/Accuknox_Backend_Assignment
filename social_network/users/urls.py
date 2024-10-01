from django.urls import path
from .views import UserSignupView, UserLoginView, LogoutView, UserSearchView, SendFriendRequestView, RespondToFriendRequestView, FriendsListView, PendingFriendRequestsView, UserActivityView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/send/<int:receiver_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/<int:request_id>/<str:action>/', RespondToFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
    path('activity/', UserActivityView.as_view(), name='user-activity'),
]
