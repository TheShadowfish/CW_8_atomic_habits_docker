from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habits
from habits.paginators import CustomPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer
from habits.services import create_periodic_task, disable_periodic_task


class HabitsCreateAPIView(generics.CreateAPIView):
    """Создание привычки для авторизованного пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()

        # Создание периодической задачи (username, habit_id, hour, minute, week_list, message, chat_id):
        hour = habit.time.hour
        minute = habit.time.minute
        # week_list = [0 - Monday, 1 - Tuesday, 2 - Wednesday, 3 - Thursday, 4 - Friday, 5 - Saturday, 6 - Sunday]
        week_list = []
        if habit.monday:
            week_list.append(0)
        if habit.tuesday:
            week_list.append(1)
        if habit.wednesday:
            week_list.append(2)
        if habit.thursday:
            week_list.append(3)
        if habit.friday:
            week_list.append(4)
        if habit.saturday:
            week_list.append(5)
        if habit.sunday:
            week_list.append(6)

        print(f"{hour}:{minute}, {week_list}")
        message = f"я буду {habit.action} в {habit.place} в {habit.time}"
        print(f"{message} to {self.request.user.tg_chat_id}")

        create_periodic_task(self.request.user.username, habit.pk, hour, minute, week_list, message,
                             self.request.user.tg_chat_id)


class HabitsListAPIView(generics.ListAPIView):
    """Отображение привычек авторизованого пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр выбранной привычки пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitsUpdateAPIView(generics.UpdateAPIView):
    """Обновление выбранной привычки пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitsDestroyAPIView(generics.DestroyAPIView):
    """Удаление выбранной привычки пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)

    def perform_destroy(self, instance):
        # Удаление периодической задачи username, habit_id)
        disable_periodic_task(self.request.user.username, instance.pk)
        super().perform_destroy(instance)


class HabitsPublicListAPIView(generics.ListAPIView):
    """Список публичных привычек"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Habits.objects.filter(is_public=True)
        return queryset
