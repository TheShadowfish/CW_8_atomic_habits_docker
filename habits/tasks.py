from datetime import datetime

from django.utils import timezone
from celery import shared_task
from habits.services import send_telegram_message
from habits.models import Habits
from users.models import User


@shared_task
def send_information_about_habit(message, tg_chat_id):
    """Отправляет сообщение пользователю о поставленном лайке"""
    # message = "Вашей собаке только что поставили лайк"
    # user = User.objects.get(email=email)
    # if user.tg_chat_id:
    send_telegram_message(message, tg_chat_id)


#
# @shared_task
# def send_email_about_birthday():
#     today = timezone.now().today().date()
#     dogs = Dog.objects.filter(owner__isnull=False, date_born=today)
#     email_list = []
#     message = "Поздравляем! У вашей собаки сегодня день рожденья!"
#     for dog in dogs:
#         email_list.append(dog.owner.email)
#         if dog.owner.tg_chat_id:
#             send_telegram_message(dog.owner.tg_chat_id, message)

@shared_task
def find_habits_in_list():
    print("Здесь будет парсится кверисет?")


class Habit:
    pass


@shared_task
def find_all_habits():

    habit_time = datetime.now().timetz().replace(second=0, microsecond=0)

    utc_time = timezone.now().today().time()

    habit_weekday = timezone.now().today().weekday()

    print(f"Все еще {habit_weekday}, {habit_time} utc {utc_time}")

    times = Habits.objects.filter(owner__isnull=False)
    count = Habits.objects.filter(owner__isnull=False).count()
    i = 0
    send_information_about_habit.delay(1567728836, f"И Т Е Р А Ц И Я {count}.len")
    for h in times:

        # print(f"Habit: {h.action}, Time: {h.time}")
        # send_information_about_habit.delay(h.owner.tg_chat_id, f"Я буду {h.action} в {h.place} в {h.time}")
        # send_information_about_habit.apply_async(args=[h.owner.tg_chat_id, f"Я

        tg_chat_id = h.owner.tg_chat_id


        print(f"h.owner {h.owner} tg_chat_id {tg_chat_id}")
        i += 1
        send_information_about_habit.delay(tg_chat_id, f"{(i)} Я {tg_chat_id}, буду (действие): ''{h.action}'' в (место) ''{h.place}'' (время): {h.time}")

    time_list = times.values_list('time', flat=True)
    print(f"Время: {time_list}")

    if habit_weekday == 0:
        print("Сегодня понедельник!")
        habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time, monday=True)
    elif habit_weekday == 1:
        print("Сегодня вторник!")
        habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time, tuesday=True)
    elif habit_weekday == 2:
        print("Сегодня среда!")
        habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time, wednesday=True)
    elif habit_weekday == 3:
        print("Сегодня четверг!")
        habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time, thursday=True)
    elif habit_weekday == 4:
        print("Сегодня пятница!")
        habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time, friday=True)
    elif habit_weekday == 5:
        print("Сегодня суббота!")
        habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time, saturday=True)
    else:
        print("Сегодня воскресенье!")
        habits = Habits.objects.filter(owner__isnull=False, utc_time=habit_time, sunday=True)

    for h in habits:
        print(f"Желание: {h.action}")
        send_information_about_habit.delay(h.owner.tg_chat_id, f"Я буду {h.action} в {h.place} в {h.time}")

    # # Здесь парсится кверисет и формируется список желаний
    # habits = Habit.objects.filter(owner__isnull=False, time=habit_time, monday=True)
    #     for habit in habits:
    #         print(f"��елание {habit.name}")
    #         send_information_about_habit.delay(f"��елание {habit.name}", habit.owner.tg_chat_id)
    #
    #
    # dogs = Habit.objects.filter(owner__isnull=False, date_born=today)
    # email_list = []
    # message = "Поздравляем! У вашей собаки сегодня день рожденья!"
    # for dog in dogs:
    #     email_list.append(dog.owner.email)
    #     if dog.owner.tg_chat_id:
    #         send_telegram_message(dog.owner.tg_chat_id, message)
    # if email_list:
    #     print(email_list)
    #     send_mail(
    #         "У вашей собаки день рожденья!",
    #         message,
    #         EMAIL_HOST_USER,
    #         email_list
    #     )
    # else:
    #     print("no emails sended today")
