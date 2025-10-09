from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from chat.models import Post, Comment, Message
from notification.models import Notification

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


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.owner:
        Notification.objects.create(
            recipient=instance.post.owner,
            sender=instance.author,
            notification_type='comment',
            message=f'{instance.author.username} прокомментировал ваш пост.'
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


@receiver(post_save, sender=Message)
def new_message_signal(sender, instance, created, **kwargs):
    if created:
        room = instance.room
        sender_user = instance.author
        recipients = room.users.exclude(id=sender_user.id)

        for user in recipients:
            Notification.objects.create(
                recipient=user,
                sender=sender_user,
                notification_type='message',
                message=f"{sender_user.username} отправил вам сообщение."
            )
