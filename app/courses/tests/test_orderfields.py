import pytest
from django.core.exceptions import ObjectDoesNotExist
from app.courses.models import Module, Content


@pytest.mark.django_db
def test_module_orderfield():
    # Создаем несколько объектов с разными значениями в поле category.
    obj1 = Module(category='A')
    obj1.save()
    obj2 = Module(category='A')
    obj2.save()
    obj3 = Module(category='B')
    obj3.save()

    # Проверяем, что поле order автоматически устанавливается и увеличивается на 1.
    assert obj1.order == 0
    assert obj2.order == 1
    assert obj3.order == 0  # Поле order не увеличивается для разных категорий.

    # Проверяем случай, когда объекты с разными категориями имеют одинаковый order.
    obj4 = Module(category='C')
    obj4.order = 1
    obj4.save()

    # Должен быть выброшен ObjectDoesNotExist, так как порядковый номер 1 уже существует.
    with pytest.raises(ObjectDoesNotExist):
        obj5 = Module(category='C')
        obj5.save()


@pytest.mark.django_db
def test_content_orderfield():
    # Создаем несколько объектов с разными значениями в поле category.
    obj1 = Content(category='A')
    obj1.save()
    obj2 = Content(category='A')
    obj2.save()
    obj3 = Content(category='B')
    obj3.save()

    # Проверяем, что поле order автоматически устанавливается и увеличивается на 1.
    assert obj1.order == 0
    assert obj2.order == 1
    assert obj3.order == 0  # Поле order не увеличивается для разных категорий.

    # Проверяем случай, когда объекты с разными категориями имеют одинаковый order.
    obj4 = Content(category='C')
    obj4.order = 1
    obj4.save()

    # Должен быть выброшен ObjectDoesNotExist, так как порядковый номер 1 уже существует.
    with pytest.raises(ObjectDoesNotExist):
        obj5 = Content(category='C')
        obj5.save()
