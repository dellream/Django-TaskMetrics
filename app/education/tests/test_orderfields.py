import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from education.models import Module, Content, Subject, Course, Text, File, Image, Video


@pytest.mark.django_db
def test_module_order():
    user = User.objects.create(username='testuser', password='testpassword')
    subject = Subject.objects.create(title='Test Subject', slug='test-subject')

    # Создаем курс и несколько модулей
    c1 = Course.objects.create(subject=subject, owner=user, title='Course 1', slug='course1')
    m1 = Module.objects.create(course=c1, title='Module 1')
    assert m1.order == 0

    m2 = Module.objects.create(course=c1, title='Module 2')
    assert m2.order == 1

    m3 = Module.objects.create(course=c1, title='Module 3', order=5)
    assert m3.order == 5

    m4 = Module.objects.create(course=c1, title='Module 4')
    assert m4.order == 6

    # Создаем второй курс и модуль
    c2 = Course.objects.create(subject=subject, owner=user, title='Course 2', slug='course2')
    m5 = Module.objects.create(course=c2, title='Module 1')
    assert m5.order == 0

    # Повторно проверяем значения полей order
    c1.refresh_from_db()
    c2.refresh_from_db()
    m1.refresh_from_db()
    m2.refresh_from_db()
    m3.refresh_from_db()
    m4.refresh_from_db()
    m5.refresh_from_db()

    assert m1.order == 0
    assert m2.order == 1
    assert m3.order == 5
    assert m4.order == 6
    assert m5.order == 0


@pytest.mark.django_db
def test_content_order():
    user = User.objects.create(username='testuser', password='testpassword')
    subject = Subject.objects.create(title='Test Subject', slug='test-subject')
    course = Course.objects.create(subject=subject, owner=user, title='Course 1', slug='course1')
    module = Module.objects.create(course=course, title='Module 1')

    # Создаем несколько объектов Content, включая Text
    text1 = Text.objects.create(owner=user, title='Text 1', content='This is text content 1')
    content1 = Content.objects.create(
        module=module,
        content_type=ContentType.objects.get_for_model(Text),
        object_id=text1.id
    )
    assert content1.order == 0

    # Создаем объекты File, Image и Video для тестирования
    file1 = File.objects.create(owner=user, title='File 1', file='path/to/file1.pdf')
    content2 = Content.objects.create(
        module=module,
        content_type=ContentType.objects.get_for_model(File),
        object_id=file1.id
    )
    assert content2.order == 1

    image1 = Image.objects.create(owner=user, title='Image 1', file='path/to/image1.jpg')
    content3 = Content.objects.create(
        module=module,
        content_type=ContentType.objects.get_for_model(Image),
        object_id=image1.id
    )
    assert content3.order == 2

    video1 = Video.objects.create(owner=user, title='Video 1', url='https://www.example.com/video1.mp4')
    content4 = Content.objects.create(
        module=module,
        content_type=ContentType.objects.get_for_model(Video),
        object_id=video1.id
    )
    assert content4.order == 3

    # Повторно проверяем значения полей order
    content1.refresh_from_db()
    content2.refresh_from_db()
    content3.refresh_from_db()
    content4.refresh_from_db()

    assert content1.order == 0
    assert content2.order == 1
    assert content3.order == 2
    assert content4.order == 3
