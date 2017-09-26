from django.contrib import messages
from django.urls import reverse
from notifications.notify import vk_messages_allowed


def resolver_context_processor(request):
    return {
        'app_name': request.resolver_match.app_name,
        'namespace': request.resolver_match.namespace,
        'url_name': request.resolver_match.url_name
    }


def remind_to_allow_messages(request):
    user = request.user
    if user.is_authenticated:
        if user.userprofile.is_subscribed and not vk_messages_allowed(user):
            messages.add_message(request, messages.INFO, '<a class="alert-link" href={}>Настроить получение уведомлений ВКонтакте</a>'
            'для оперативного информарования о рассмотрении заявлений на матпомощь, обращений в Сенат и т.д.'
                                 .format(reverse("blog:article_detail", args=["notifications"])))
    return {}