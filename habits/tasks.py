from celery import shared_task

from habits.services import send_telegram_message


@shared_task
def send_information_about_habit(message, tg_chat_id):
    """Отправляет сообщение пользователю о поставленном лайке"""
    # message = "Вашей собаке только что поставили лайк"
    # user = User.objects.get(email=email)
    # if user.tg_chat_id:
    send_telegram_message(tg_chat_id, message)

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

