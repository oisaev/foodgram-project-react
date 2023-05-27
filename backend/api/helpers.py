from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from users.models import Subscription
from .serializers import SubscriptionSerializer

User = get_user_model()


def subscribe(request, subscribed_id):
    subscribed = get_object_or_404(User, id=subscribed_id)
    if subscribed == request.user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    instance = Subscription.objects.filter(
        subscriber=request.user,
        subscribed=subscribed
    )
    if not instance.exists():
        subscription = Subscription.objects.create(
            subscriber=request.user,
            subscribed=subscribed
        )
        serialized = SubscriptionSerializer(subscription)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def unsubscribe(request, subscribed_id):
    subscribed = get_object_or_404(User, id=subscribed_id)
    instance = Subscription.objects.filter(
        subscriber=request.user,
        subscribed=subscribed
    )
    if instance.exists():
        Subscription.objects.filter(
            subscriber=request.user,
            subscribed=subscribed
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
