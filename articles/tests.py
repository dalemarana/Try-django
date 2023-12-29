from django.test import TestCase
from django.utils.text import slugify
# Create your tests here.
from .models import Article
from .utils import slugify_instance_title

class ArticleTestCase(TestCase):
    # to allow to create entries to test database
    def setUp(self):
        # loop to several times
        self.number_of_articles = 50_000
        for i in range(0, self.number_of_articles):
            Article.objects.create(title='Hello world', content='something else')

    # test if database is there
    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    # test the count in the database
    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)

    # test the 1st slug equal to actual
    def test_hello_world_slug(self):
        obj = Article.objects.all().order_by("id").first()
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title)
        
    # test slug excluding 1st
    def test_hello_world_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)

    # test title
    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for i in range(0, 25):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_slugify_instance_title_redux(self):
        slug_list = Article.objects.all().values_list('slug', flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_slug_list))

    # def test_user_added_slug_unique(self)