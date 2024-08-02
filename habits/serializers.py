from rest_framework import serializers

from habits.models import Habits
from habits.validators import HabitsDurationValidator, HabitsPeriodicyValidator


class HabitSerializer(serializers.ModelSerializer):
    validators = [HabitsDurationValidator(field='duration'), HabitsPeriodicyValidator(field='periodicity')]
    class Meta:
        model = Habits
        fields = '__all__'
        # validators = [HabitsValidator]

    def validate(self, data):
        # У приятной привычки не может быть вознаграждения или связанной привычки.
        if data.get('is_nice'):
            if data.get('related') or data.get('prize'):
                raise serializers.ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')

        # Исключить одновременный выбор связанной привычки и указания вознаграждения.
        # В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей.
        if data.get('related') and data.get('prize'):
             raise serializers.ValidationError('Может быть либо связанная привычка либо вознаграждение,')

        # В связанные привычки могут попадать только привычки с признаком приятной привычки.
        if data.get('related'):
            if not data.get('related').is_nice:
                  raise serializers.ValidationError('Связанные привычки = приятные привычки')

        return data

# class PublicHabitSerializer(serializers.ModelSerializer):
#     queryset = Habits.objects.filter(is_public=True)
#     validators = [HabitsDurationValidator(field='duration'), HabitsPeriodicyValidator(field='periodicity')]
#
#     class Meta:
#         model = Habits
#         fields = '__all__'
#
#     def validate(self, data):
#         raise serializers.ValidationError('Привычка может быть создана только индивидуальноб список публичных привычек недоступен для редактирования')