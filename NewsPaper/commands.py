#1 Создание пользователей

from django.contrib.auth.models import User

user=User.objects.create_user('User1', password='User1')
user=User.objects.create_user('User2', password='User2')
user.is_superuser=False
user.is_staff=False
user.save()

#2 Создать два объекта модели Author, связанные с пользователями

from news.models import *
User.objects.all()
<QuerySet [<User: admin>, <User: User1>, <User: User2>]>
u1 = User.objects.get(username='User1')
Author.objects.create(user=u1, rating='1')
<Author: Author object (1)>
u1.save()
u2 = User.objects.get(username='User2')
Author.objects.create(user=u2, rating='2')
<Author: Author object (2)>
u2.save()


#3 Добавить 4 категории в модель Category
from news.models import Category
category_1 = Category.objects.create(category_name='Наука')
category_2 = Category.objects.create(category_name='Спорт')
category_3 = Category.objects.create(category_name='Обо всем')
category_4 = Category.objects.create(category_name='Туризм')
category_5 = Category.objects.create(category_name='Разное')

#4 Добавить 2 статьи и 1 новость

from news.models import *
post_news1 = Post.objects.create(author=Author.objects.get(pk=1), title='Ученые изобрели телеском Джеймс Уэбб', text='Самый мощный телескоп', choice='news')
post_art1 = Post.objects.create(author=Author.objects.get(pk=1), title='Немецкая Бавария вновь уверенно обыгрывает', text='Левандовски хет-трик ', choice='articles')
post_art2 = Post.objects.create(author=Author.objects.get(pk=2), title='Торнадо над Канадой', text='Эвакуация людей или укрытие в домах?', choice='articles')

#5 Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
from news.models import *

category_1 = Category.objects.all()[0]
category_2 = Category.objects.all()[1]
category_3 = Category.objects.all()[2]
category_4 = Category.objects.all()[3]
category_5 = Category.objects.all()[4]
post_news1.category.add(category_1)
post_art1.category.add(category_2)
post_art2.category.add(category_3, category_5)

#6 Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).

from news.models import Comment

post_news1 = Post.objects.get(pk=4)
comment_1 = Comment.objects.create(comment_user=User.objects.get(pk=1), comment_post=post_news1, comment_text='Надо узнать почем телескоп?)')
post_news1 = Post.objects.get(pk=5)
comment_2 = Comment.objects.create(comment_user=User.objects.get(pk=1), comment_post=post_news1, comment_text='Качество звезд отличное')
post_art1 = Post.objects.get(pk=5)
comment_3 = Comment.objects.create(comment_user=User.objects.get(pk=1), comment_post=post_art1, comment_text='Немцы всегда машина')
post_art2 = Post.objects.get(pk=6)
comment_4 = Comment.objects.create(comment_user=User.objects.get(pk=2), comment_post=post_art2, comment_text='Ого, не поеду в этом году в Канаду')

#7 Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
post_news1.like()
post_news1.like()
post_news1.like()
post_art1.like()
post_art2.like()
comment_1.like()
comment_3.dislike()
comment_4.dislike()
post_art1.like()
post_art2.like()
post_art2.like()
post_news1.dislike()

#8 Обновить рейтинги пользователей.

author_1 = Author.objects.get(pk=1)
author_1.update_rating()

author_2 = Author.objects.get(pk=2)
author_2.update_rating()

#9 Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
Author.objects.all().order_by('-rating').values('user__username', 'rating').first()

#10 Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
best_post = Post.objects.all().order_by('-post_rating').first()
best_post_data = Post.objects.all().order_by('-post_rating').values('posting_time', 'author__user__username', 'post_rating', 'title').first()
best_post_preview = Post.objects.all().order_by('-post_rating').first().preview()
best_post_preview
'Левандовски хет-трик ...'

#11 Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

comments = Comment.objects.filter(comment_post = best_post).values('comment_date', 'comment_user', 'comment_rating', 'comment_text')
comments
<QuerySet [{'comment_date': None, 'comment_user': 1, 'comment_rating': 0, 'comment_text': 'Качество звезд отличное'}, {'comment_date': None, 'comment_user': 1, 'comment_rating': -1, 'comment_text': 'Немцы всегда машина'}]>

