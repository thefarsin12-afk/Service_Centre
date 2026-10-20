from django.urls import path

from service.views import UserRegistrationView,GetMeView
from service.views import SeriviceRequestCreateList,ServiceRequestRetriveUpdateDelete
from service.views import FilterView
from service.views import SerachView
from service.views import PendingServiceView
from service.views import SummaryServiceView
from service.views import HighCriticalServiceView

urlpatterns = [

    path('user/',UserRegistrationView.as_view()),

    path("user/me/",GetMeView.as_view()),

    path('request/',SeriviceRequestCreateList.as_view()),

    path('request/<int:pk>/',ServiceRequestRetriveUpdateDelete.as_view()),

    path('request/filter/',FilterView.as_view()),

    path('request/search/',SerachView.as_view()),

    path('request/pending/',PendingServiceView.as_view()),

    path('request/summary/',SummaryServiceView.as_view()),

    path('request/priority/',HighCriticalServiceView.as_view())
]