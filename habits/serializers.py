from rest_framework import serializers

from habits.models import Habits
from habits.validators import HabitsDurationValidator, HabitsPeriodicValidator


class HabitSerializer(serializers.ModelSerializer):
    validators = [HabitsDurationValidator(field="duration"), HabitsPeriodicValidator(field="periodicity")]

    class Meta:
        model = Habits
        fields = "__all__"
        # validators = [HabitsValidator]

    def validate(self, data):
        """
        У приятной привычки не может быть вознаграждения или связанной привычки. Исключить одновременный выбор
        связанной привычки и указания вознаграждения. В модели не должно быть заполнено одновременно и поле
        вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей.
        """

        if data.get("related") and data.get("prize"):
            raise serializers.ValidationError("Может быть либо связанная привычка либо вознаграждение,")

        if data.get("is_nice"):
            if data.get("related") or data.get("prize"):
                raise serializers.ValidationError("У приятной привычки не может быть связанной привычки или "
                                                  "вознаграждения")

        # В связанные привычки могут попадать только привычки с признаком приятной привычки.
        if data.get("related") and (not data.get("related").is_nice):
            raise serializers.ValidationError("Связанные привычки = приятные привычки")

        # Хотя бы один день в неделю
        if (data.get("sunday") is False and data.get("monday") is False and data.get("tuesday") is False
                and data.get("thursday") is False and data.get("friday") is False and data.get("saturday") is False
                and data.get("wednesday") is False):
            raise serializers.ValidationError("Хотя бы один день в неделю должен быть выбран!")

        return data
