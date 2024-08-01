from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits
from users.models import User


class HabitTestCase(APITestCase):
    """ Тестирование модели Habits """

    def setUp(self):
        """ Создание тестовой модели Пользователя (с авторизацией) и Привычки """

        self.user = User.objects.create(
            email="test@test.com",
            password="testpassword",
            tg_chat_id='1567728836'
        )
        self.client.force_authenticate(user=self.user)
        self.habit = Habits.objects.create(
            owner=self.user,
            place="Магазин",
            time="18:00:00",
            action="Пойти в магазин за покупками",
            periodicity=1,
            duration=60
        )
        # is_good = models.BooleanField(default=True, verbose_name='Приятная', choices=IS_GOOD_CHOICES)
        # related = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная с другой привычкой',                                     **NULLABLE)
        # prize = models.CharField(max_length=100, verbose_name='Вознаграждение', **NULLABLE)
        # is_public = models.BooleanField(default=True, verbose_name='Публичная', choices=PUBLIC_CHOICES)

    def test_create_habit(self):
        """ Тестирование создания привычки """

        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Магазин",
            "time": "18:00:00",
            "action": "Пойти в магазин за покупками",
            "duration": 60,
            "periodicity": 1
        }

        response = self.client.post(url, data=data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("owner"), self.user.pk)
        self.assertEqual(data.get("place"), "Магазин")
        self.assertEqual(data.get("time"), "18:00:00")
        self.assertEqual(data.get("action"), "Пойти в магазин за покупками")
        self.assertEqual(data.get("duration"), 60)
        self.assertEqual(data.get("periodicity"), 1)

    def test_create_habit_validators(self):
        """ Тестирование работы валидаиора """

        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Магазин",
            "time": "18:00:00",
            "action": "Пойти в магазин за покупками",
            "duration": 180,
            "periodicity": 1
        }

        response = self.client.post(url, data=data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_habit(self):
        """ Тестирование вывода всех привычек """
        url = reverse('habits:habits_list')
        response = self.client.get(url)
        data = response.json()


        created_text = str(self.habit.created_at)
        created = created_text[0:10] + 'T' + created_text[11:26] + 'Z'
        updated_text = str(self.habit.updated_at)
        updated = updated_text[0:10] + 'T' + updated_text[11:26] + 'Z'
        # print(f"created {created}")
        # print(f"updated {updated}")

        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results':
                [
                    {
                        'id': self.habit.pk,
                        'owner': self.user.pk,
                        'place': "Магазин",
                        'time': "18:00:00",
                        'action': "Пойти в магазин за покупками",
                        'is_good':True,
                        'related':None,
                        'periodicity':1,
                        'prize':None,
                        'duration': 60,
                        'is_public':True,
                        'created_at': created,
                        'updated_at': updated
                    }
                ]
        }


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_retrieve_habit(self):
        """ Тестирование просмотра одной привычки """

        url = reverse("habits:habits_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("owner"), self.habit.owner.id)
        self.assertEqual(data.get("place"), self.habit.place)
        self.assertEqual(data.get("time"), self.habit.time)
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("duration"), self.habit.duration)
        self.assertEqual(data.get("periodicity"), self.habit.periodicity)

    def test_update_habit(self):
        """ Тестирование изменений привычки """

        url = reverse("habits:habits_update", args=(self.habit.pk,))
        data = {
            "owner": self.user.pk,
            "place": "Фитнес-зал",
            "time": "19:00:00",
            "action": "Тренировка в фитнес-зале",
            "duration": 120,
            "periodicity": 1,
        }
        response = self.client.put(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("owner"), self.habit.owner.id)
        self.assertEqual(data.get("place"), "Фитнес-зал")
        self.assertEqual(data.get("time"), "19:00:00")
        self.assertEqual(data.get("action"), "Тренировка в фитнес-зале")
        self.assertEqual(data.get("duration"), 120)
        self.assertEqual(data.get("periodicity"), 1)

    def test_delete_habit(self):
        """ Тестирование удаления привычки """

        url = reverse("habits:habits_delete", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_public_habit(self):
        """ Тестирование вывода публичных привычек """
        url = reverse('habits:habits_list')
        response = self.client.get(url)
        data = response.json()
        created_text = str(self.habit.created_at)
        created = created_text[0:10] + 'T' + created_text[11:26] + 'Z'
        updated_text = str(self.habit.updated_at)
        updated = updated_text[0:10] + 'T' + updated_text[11:26] + 'Z'
        # print(f"created {created}")
        # print(f"updated {updated}")

        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results':
                [
                    {
                        'id': self.habit.pk,
                        'owner': self.user.pk,
                        'place': "Магазин",
                        'time': "18:00:00",
                        'action': "Пойти в магазин за покупками",
                        'is_good': True,
                        'related': None,
                        'periodicity': 1,
                        'prize': None,
                        'duration': 60,
                        'is_public': True,
                        'created_at': created,
                        'updated_at': updated
                    }
                ]
        }

        response = self.client.get(reverse('habits:public_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
