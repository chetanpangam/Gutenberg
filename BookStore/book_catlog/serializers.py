from rest_framework import serializers
from .models import *



class QueryParamSerializer(serializers.Serializer):
    author = serializers.CharField(max_length=100, required=False)
    language = serializers.CharField(max_length=100, required=False)
    topic = serializers.CharField(required=False)
    mime_type = serializers.CharField(required=False)
    book_id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)

class AutherSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = BooksAuthor
        fields = ["name"]

class BookShelfSerializer(serializers.ModelSerializer):

    class Meta:
        model = BooksBookshelf
        fields = ["name"]

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BooksLanguage
        fields = ["code"]

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = BooksSubject
        fields = ["name"]

class FormatSerializer(serializers.ModelSerializer):

    class Meta:
        model = BooksFormat
        fields = ["mime_type", "url"]

class BookSerializer(serializers.ModelSerializer):
    authors = AutherSerializer(many=True)
    language = LanguageSerializer(many=True)
    bookshelf = BookShelfSerializer(many=True)
    subject = SubjectSerializer(many=True)
    format = FormatSerializer(many=True, read_only=True)

    class Meta:
        model = BooksBook
        fields = ["gutenberg_id", "title", "download_count", "authors", "language", "bookshelf", "subject", "format"]
    
