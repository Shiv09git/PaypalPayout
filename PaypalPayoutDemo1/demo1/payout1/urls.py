from django.urls import path

# from demo1.payout1 import paypal_client
from .views import paypal_payout,PAL, cpo, pitmid, gpo
# from .paypal_client import PAL

urlpatterns=[
    path('withdraw/', paypal_payout),
    path('cpo/', cpo),
    # path('cpo/', CreatePayouts),
    path('tr/', PAL),
    path('pbi/', gpo),
    path('piid/', pitmid)

]