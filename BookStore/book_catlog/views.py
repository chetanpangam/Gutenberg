from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import BooksBook, BooksFormat
from django.db.models import F, Q
from .serializers import BookSerializer, QueryParamSerializer
from rest_framework.exceptions import ValidationError

# Create your views here.

class BookCatalogView(ListAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        print(self.request.query_params)
        
        serializer = QueryParamSerializer(data=self.request.query_params)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        validated_data = serializer.validated_data
        print(validated_data)
    
        gutenberg_id = validated_data.get('book_id', None)
        language = validated_data.get('language', None)
        mime_type = validated_data.get('mime_type', None)
        topic = validated_data.get('topic', None)
        author = validated_data.get('author', None)
        title = validated_data.get('title', None)

        queryset = BooksBook.objects.all()

        if gutenberg_id:
            queryset = queryset.filter(gutenberg_id=gutenberg_id)
        
        if language:
            queryset = queryset.filter(language__code=language)

        if topic:
            queryset = queryset.filter(Q(bookshelf__name__icontains=topic) | Q(subject__name__icontains=topic))

        if mime_type:
            queryset = queryset.filter(booksformat__mime_type=mime_type)

        if author:
            queryset = queryset.filter(authors__name__icontains=author)

        if title:
            queryset = queryset.filter(title__icontains=title)

        queryset = queryset.order_by(F('download_count').desc(nulls_last=True))
        
        return queryset
