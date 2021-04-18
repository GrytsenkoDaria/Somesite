from django.db import models
from django.contrib.auth.models import User


class ProductType(models.TextChoices):
    SNEAKERS = 'Кросовки'   # Создаю класс 'ProductType', класс выбора, в нем я обьявляю свои переменные (Теги
    GUMSHOES = 'Кеды'   # по которым я буду сортировать/фильтровать), название с большой буквы
    # этот класс нужно передать в CharField моей основной модели ( в моем случае 'Product' )


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    create_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Время в живую поскольку параметр Тру
    name = models.CharField(max_length=30, verbose_name='Имя')  # Максимальна длина строки
    text = models.TextField()   # Тест ( много текста ) в отличии от 'CharField' Который принимает определенное
    # кол-то текста, 'TextField' принимет инфинити текста.
    price = models.IntegerField(null=True, verbose_name='Цена')
    image = models.ImageField(default='images/no.png', upload_to='images/', null=True, blank=True, verbose_name='Картинка')
    type = models.CharField(choices=ProductType.choices, max_length=40)  # 'choices' передаю свой класс 'ProductType'
    # null=True означет что в базе данных может
    # быть пустое место, может и не быть картинки, blank=True в запросте на бэкенд может не приходить.
    # type = models.ForeignKey('ProductType', null=True, on_delete=models.PROTECT, verbose_name='Категория')
    #PROTECT = если я удалю тип(связь) то моя модель ( Кверисет ) останеться
    #CASCADE = если я удалю свою свзять (тип) то модель ( кверисет ) тоже удалиться


    def __str__(self):
        return self.name

    class Meta:
        pass
        # ordering = [
        #     '-create_data',
        #     'price'
        # ]