from rest_framework import serializers


class HabitsValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        value = dict(value)

        if value.get('is_good'):
            if value.get('related') or value.get('prize'):
                raise serializers.ValidationError(
                    'У приятной привычки не может быть связанной привычки или вознаграждения')
            if value.get('related') and value.get('prize'):
                raise serializers.ValidationError(
                    'Может быть связанная привычка или вознаграждение,')


            if value.get('duration') > 120:
                print(value.get('duration'))
                raise serializers.ValidationError(
                    'Длительность привычки не может быть больше 2 часов')
            if value.get('related'):
                if not value.get('related').is_good:
                    raise serializers.ValidationError('Связанные привычки = приятные привычки')
            if 7 > value.get('periodicity') or value.get('periodicity') < 1:
                raise serializers.ValidationError('Привычка должна иметь периодичность повторения от 1 раза в день до 1 (1) раза в 7 дней (7)')