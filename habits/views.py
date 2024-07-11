from django.shortcuts import render
from rest_framework import generics

from habits.models import Habits
from habits.serializers import HabitSerializer


class HabitsCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    # permission_classes = (IsAuthenticated, IsOwner)

    # def perform_create(self, serializer):
    #     habit = serializer.save()
    #     habit.owner = self.request.user
    #     habit.save()


class HabitsListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    # permission_classes = (IsAuthenticated, )
    # pagination_class = CustomPagination
    #
    # def get_queryset(self):
    #     queryset = self.queryset.filter(owner=self.request.user)
    #     return queryset


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    # permission_classes = (IsAuthenticated, IsOwner)


class HabitsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    # permission_classes = (IsAuthenticated, IsOwner)


class HabitsDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    # permission_classes = (IsAuthenticated, IsOwner)


class HabitsPublicListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habits.objects.filter(is_public=True)
    # permission_classes = (AllowAny, )
    # pagination_class = CustomPagination
