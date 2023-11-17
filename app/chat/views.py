from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
import logging

from django.views import View

from education.models import Course

logger = logging.getLogger(__name__)


class TestLoggingView(View):
    def get(self, request, *args, **kwargs):
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        return HttpResponse("Logging test view")


@login_required
def course_chat_room(request, course_id):
    try:
        # извлечь курс с заданным id, к которому
        # присоединился текущий пользователь
        course = request.user.courses_joined.get(id=course_id)
    except (Course.DoesNotExist, ValueError) as e:
        # Course.DoesNotExist - курс не существует
        # ValueError - возникает при некорректном значении course_id
        logger.error(e)
        return HttpResponseForbidden("Некорректный курс или курс не найден.")
    return render(
        request,
        'chat/room.html',
        {
            'course': course
        }
    )
