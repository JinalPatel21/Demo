from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Category, Article
from django.contrib.auth.models import User

@registry.register_document
class UserDocument(Document):
    class Index:
        name = "users"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = User
        fields = ["id", "first_name", "last_name"]

@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = "categories"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Category
        fields = ["id", "name", "description"]


@registry.register_document
class ArticleDocument(Document):
    author = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "username": fields.TextField(),
        "first_name": fields.TextField(),
        "last_name": fields.TextField(),
    })
    categories = fields.NestedField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
        "description": fields.TextField(),
    })
    type = fields.TextField(attr="type_to_string")

    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "created_datetime",
            "updated_datetime",
        ]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.article_set.all()
        elif isinstance(related_instance, Category):
            return related_instance.articles.all()
