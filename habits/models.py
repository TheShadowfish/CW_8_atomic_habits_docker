from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {'blank': True, 'null': True}

"""
**Привычка:**

- Пользователь — создатель привычки.
- Место — место, в котором необходимо выполнять привычку.
- Время — время, когда необходимо выполнять привычку.
- Действие — действие, которое представляет собой привычка.
- Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
- Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.
- Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.
- Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
- Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
- Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.

Полезная привычка — это само действие, которое пользователь будет совершать и получать за его выполнение определенное вознаграждение (приятная привычка или любое другое вознаграждение).
Приятная привычка — это способ вознаградить себя за выполнение полезной привычки. Приятная привычка указывается в качестве связанной для полезной привычки (в поле «Связанная привычка»).
Признак приятной привычки — булево поле, которые указывает на то, что привычка является приятной, а не полезной.
"""

class Habits(models.Model):

    PERIOD_CHOICES = (
        (True, 'Ежедневная'),
        (False, 'Еженедельная'),
    )

    IS_GOOD_CHOICES = (
        (True, 'Приятная'),
        (False, 'Нет'),
    )

    PUBLIC_CHOICES = (
        (True, 'Публичная'),
        (False, 'Нет'),
    )
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=140, verbose_name='Место')
    time = models.TimeField(verbose_name='Время, когда надо выполнить привычку')
    action = models.CharField(max_length=140, verbose_name='Действие, которое надо сделать')
    is_good = models.BooleanField(default=True, verbose_name='Приятная', choices=IS_GOOD_CHOICES)
    related = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная с другой привычкой', **NULLABLE)
    periodicity = models.SmallIntegerField(default=1, verbose_name='Периодичность (в днях) - от 1 до 7')
    prize = models.CharField(max_length=100, verbose_name='Вознаграждение', **NULLABLE)
    duration = models.SmallIntegerField(verbose_name='Время на выполнение (в минутах)')
    is_public = models.BooleanField(default=True, verbose_name='Публичная', choices=PUBLIC_CHOICES)

    created_at = models.DateTimeField(**NULLABLE, verbose_name="Дата создания", help_text="Укажите дату создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(**NULLABLE, verbose_name="Дата изменения", help_text="Укажите дату изменения",
        auto_now=True,
    )

     # is_daily = models.BooleanField(default=False, choices=PERIOD_CHOICES, verbose_name='Периодичность')


    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-id']

