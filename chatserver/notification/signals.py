from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from booking.models import Booking
from chat.models import Post, Comment, Message, CommunityMembership
from notification.models import Notification
from notification.tasks import send_email_notification

User = get_user_model()


@receiver(m2m_changed, sender=Post.likes.through)
def create_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            sender_user = User.objects.get(pk=user_id)
            if sender_user != instance.owner:  # чтобы не уведомлять самого себя
                Notification.objects.create(
                    recipient=instance.owner,
                    sender=sender_user,
                    notification_type='like',
                    message=f'{sender_user.username} лайкнул ваш пост.'
                )
                send_email_notification.delay(
                    subject='Вашу публикацию оценили',
                    message=f'Пользователь {sender_user} оценил вашу публикацию',
                    recipient_list=[instance.owner.email]
                )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.owner:
        Notification.objects.create(
            recipient=instance.post.owner,
            sender=instance.author,
            notification_type='comment',
            message=f'{instance.author.username} прокомментировал ваш пост.'
        )
    send_email_notification.delay(
        subject='Ваш пост прокоментировали',
        message=f'Ваш пост {instance.post.id} прокоментировал {instance.author.username}',
        recipient_list=[instance.post.owner.email]
    )


@receiver(m2m_changed, sender=User.friend_requests.through)
def friend_request_signal(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            recipient = User.objects.get(pk=user_id)
            Notification.objects.create(
                recipient=recipient,
                sender=instance,
                notification_type='friend_request',
                message=f"{instance.username} отправил вам заявку в друзья."
            )
            send_email_notification.delay(
                subject='Вам пришла заявка в друзья',
                message=f'Вам пришел запрос в друзья от: {instance.username}',
                recipient_list=[recipient.email]
            )


@receiver(post_save, sender=Message)
def new_message_signal(sender, instance, created, **kwargs):
    if created:
        room = instance.room
        sender_user = instance.author
        recipients = room.users.exclude(id=sender_user.id)
        text = instance.text

        for user in recipients:
            Notification.objects.create(
                recipient=user,
                sender=sender_user,
                notification_type='message',
                message=f"{sender_user.username} отправил вам сообщение."
            )

            send_email_notification.delay(
                subject='Вам пришло сообщение',
                message=f'Вам пришло сообщение от {sender_user.username}: {text}',
                recipient_list=[user.email]
            )


@receiver(post_save, sender=CommunityMembership)
def community_join_notification(sender, instance, created, **kwargs):
    if created:
        community = instance.community
        new_member = instance.user
        owner = community.owner

        if new_member == owner:
            return

        Notification.objects.create(
            recipient=owner,
            sender=new_member,
            notification_type='community_join',
            message=f"{new_member.username} вступил в ваше сообщество '{community.name}'."
        )

        send_email_notification.delay(
            subject='Новый участник в вашем сообществе',
            message=f"Пользователь {new_member.username} вступил в ваше сообщество '{community.name}'.",
            recipient_list=[owner.email]
        )


@receiver(post_save, sender=Booking)
def community_join_notification(sender, instance, created, **kwargs):
    if created:
        event_type = instance.event_type
        guest = instance.guest
        owner = event_type.owner
        start_time = instance.start_time
        date_time = instance.date

        Notification.objects.create(
            recipient=owner,
            sender=guest,
            notification_type='booking',
            message=f'Пользователь {guest.username} забронировал созвон {event_type} {date_time} в {start_time}'
        )

        send_email_notification.delay(
            subject='Новый участник в вашем сообществе',
            message=f"Пользователь {guest.username} забронировал созвон {event_type} {date_time} в {start_time}",
            recipient_list=[owner.email]
        )
