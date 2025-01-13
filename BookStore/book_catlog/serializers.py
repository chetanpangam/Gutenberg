from rest_framework import serializers
from .models import *


class QueryParamSerializer(serializers.Serializer):
    
    author = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False)
    language = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False)
    topic = serializers.ListField(
        child=serializers.CharField(), required=False)
    mime_type = serializers.ListField(
        child=serializers.CharField(), required=False)
    book_id = serializers.ListField(
        child=serializers.IntegerField(), required=False)
    title = serializers.ListField(
        child=serializers.CharField(),required=False)

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
        fields = ["url"]

class BookSerializer(serializers.ModelSerializer):
    authors = AutherSerializer(many=True)
    language = LanguageSerializer(many=True)
    bookshelf = BookShelfSerializer(many=True)
    subject = SubjectSerializer(many=True)
    formats = FormatSerializer(many=True) 

    class Meta:
        model = BooksBook
        fields = ["title", "authors", "language", "bookshelf", "subject", "formats"]
    
