from rest_framework import serializers


class HabitsDurationValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = dict(value).get(self.field)
        if duration > 120:
            raise serializers.ValidationError("Длительность привычки не может быть больше 120 минут")
