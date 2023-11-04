from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
    Поле для автоматического упорядочивания объектов в модели.

    Это поле автоматически назначает порядковый номер объектам в модели.
    Он ищет последний порядковый номер для объектов, связанных с теми
    же полями, указанными в `for_fields`, и увеличивает его на 1.

    Аргументы:
    - `for_fields` (list): Список полей модели, для которых вы хотите
     упорядочить объекты.

    Пример использования:

    class ExampleModel(models.Model):
       order = OrderField(for_fields=['category'])

    В этом примере, объекты MyModel будут автоматически упорядочиваться
    по полю 'order' в пределах одинаковой категории.
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.for_fields = for_fields

    def pre_save(self, model_instance, add):
        """
        Вычисляет порядковый номер и назначает его объекту перед сохранением.
        """
        # Если порядковый номер уже назначен объекту, ничего не делаем.
        if getattr(model_instance, self.attname) is not None:
            return super().pre_save(model_instance, add)
        else:
            try:
                qs = self.model.objects.all()
                #
                if self.for_fields:
                    query = {
                        # Создает словарь для фильтрации объектов по полям.
                        field: getattr(model_instance, field) for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                # Ищет последний объект и получает его порядковый номер.
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                # Если объект не найден, присваивает начальное значение.
                value = 0

            # Присваивает порядковый номер объекту и возвращает его.
            setattr(model_instance, self.attname, value)
            return value
