from rest_framework import serializers

# """
# - Исключить одновременный выбор связанной привычки и указания вознаграждения.
# - В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей.
#
# - В связанные привычки могут попадать только привычки с признаком приятной привычки.
# - У приятной привычки не может быть вознаграждения или связанной привычки.
#
# """
#
# def validate_fields_logic(validated_data):
#     value = dict(validated_data)
#
#     if validated_data.get('is_good'):
#         if validated_data.get('related') or value.get('prize'):
#             raise serializers.ValidationError('У приятной привычки не может быть связанной привычки или вознаграждения')
#         if validated_data.get('related') and validated_data.get('prize'):
#             raise serializers.ValidationError('Может быть связанная привычка или вознаграждение,')
#
#         if validated_data.get('related'):
#             if not validated_data.get('related').is_good:
#                 raise serializers.ValidationError('Связанные привычки = приятные привычки')



class HabitsPeriodicyValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = dict(value).get(self.field)
        if 7 < periodicity or periodicity < 1:
            raise serializers.ValidationError('Привычка должна иметь период повторения от 1 дня до 7 дней.')

class HabitsDurationValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        duration = dict(value).get(self.field)
        if duration > 120:
            raise serializers.ValidationError('Длительность привычки не может быть больше 120 минут')


# class HabitsValidator:
#     def __init__(self, field):
#         self.field = field
#
#     def __call__(self, value):
#         value = dict(value)
#
#         if value.get('is_good'):
#             if value.get('related') or value.get('prize'):
#                 raise serializers.ValidationError(
#                     'У приятной привычки не может быть связанной привычки или вознаграждения')
#             if value.get('related') and value.get('prize'):
#                 raise serializers.ValidationError(
#                     'Может быть связанная привычка или вознаграждение,')
#
#
#             if value.get('duration') > 120:
#                 print(value.get('duration'))
#                 raise serializers.ValidationError(
#                     'Длительность привычки не может быть больше 2 часов')
#             if value.get('related'):
#                 if not value.get('related').is_good:
#                     raise serializers.ValidationError('Связанные привычки = приятные привычки')
#             if 7 > value.get('periodicity') or value.get('periodicity') < 1:
#                 raise serializers.ValidationError('Привычка должна иметь периодичность повторения от 1 раза в день до 1 (1) раза в 7 дней (7)')