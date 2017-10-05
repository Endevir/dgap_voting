from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

import logging

from fin_aid.models import AidRequest
from profiles.models import UserProfile
from cycle_storage.models import Bicycle
from .notify import notify, notify_group, vk_messages_allowed
from .templates import fin_aid_new_request, fin_aid_request_status_change, bicycle_request_status_change, bicycle_new_request
from .models import UserNotificationsSettings

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AidRequest, dispatch_uid='notifications')
def aidrequest_save_notify(sender, instance, created, **kwargs):
    # AirRequestCreate view form_valid() method creates aid request, ONLY THEN adds current user to it.
    # So when 'create' signal received, there is no aidrequest.applicant yet
    try:
        if not created:
            if instance.status == AidRequest.WAITING and instance.category.notifications:
                try:
                    text = fin_aid_new_request(instance)
                except Exception as e:
                    text = "Новое заявление на матпомощь"
                    logger.exception(e)
                notify_group('finance', text)
            else:
                if instance.status != AidRequest.WAITING:
                    try:
                        text = fin_aid_request_status_change(instance)
                    except Exception as e:
                        text = "Изменен статус заявления на матпомощь"
                        logger.exception(e)
                    notify(instance.applicant, text)
    except Exception as e:
        logger.exception(e)


@receiver(post_save, sender=UserProfile, dispatch_uid='notifications')
def user_create(sender, instance, created, **kwargs):
    settings, created = UserNotificationsSettings.objects.get_or_create(user=instance.user)
    settings.allow_vk = instance.is_subscribed
    settings.save()


@receiver(user_logged_in, dispatch_uid='notifications')
def remind_to_allow_messages(sender, request, **kwargs):
    user = request.user
    try:
        settings = user.usernotificationssettings
        if user.userprofile.is_subscribed and not vk_messages_allowed(user) and not settings.last_allow_vk_reminder:
            messages.add_message(request, messages.INFO, '<a class="alert-link" href={}>Настроить получение уведомлений ВКонтакте</a> '
            'для оперативного информирования о рассмотрении заявлений на матпомощь, обращений в Сенат и т.д.'
                                 .format(reverse("blog:article_detail", args=["notifications"])))
        settings.last_allow_vk_reminder = timezone.now()
        settings.save()
    except Exception:
        pass


@receiver(post_save, sender=Bicycle, dispatch_uid='notifications')
def bicycle_save_notify(sender, instance, created, **kwargs):
    # BicycleCreate view form_valid() method creates aid request, ONLY THEN adds current user to it.
    # So when 'create' signal received, there is no aidrequest.applicant yet
    try:
        if not created:
            if instance.status == AidRequest.WAITING:
                users = User.objects.filter(groups__name='bicycle')
                text = bicycle_new_request(instance)
                notify_group('bicycle', text)
            else:
                if instance.status != AidRequest.WAITING:
                    text = bicycle_request_status_change(instance)
                    notify(instance.applicant, text)
    except Exception as e:
        logger.exception(e)
