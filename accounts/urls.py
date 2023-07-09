from django.urls import path
from .views import (my_account_view,
    invite_received_view, 
    accounts_list_view, 
    AccountDetailView,
    AccountListView,
    send_invitation,
    remove_connection,
    confirm_invitation,
    decline_invitation,
    
)

app_name = 'accounts'

urlpatterns = [
    path('', AccountListView.as_view(), name='all-accounts-view'),
    path('myaccount/', my_account_view, name='my-account-view'),
    path('my-invitations/', invite_received_view, name='my-invitations-view'),
    path('send-invitation/', send_invitation, name='send-invite'),
    path('remove-connection/', remove_connection, name='remove-connection'),
    path('<slug>/', AccountDetailView.as_view(), name='account-detail-view'),
    path('my-invitations/confirm/', confirm_invitation, name='confirm-invite'),
    path('my-invitations/decline/', decline_invitation, name='decline-invite'),
]


