from rest_framework.generics import ListAPIView
from .models import BooksBook, BooksFormat
from django.db.models import F, Q, Prefetch
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
        param_dict = {}
        for parameter, values in self.request.query_params.items():
            param_dict[parameter] = values.split(',')
        
        serializer = QueryParamSerializer(data=param_dict)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        validated_data = serializer.validated_data
    
        gutenberg_id = validated_data.get('book_id', None)
        languages = validated_data.get('language', None)
        mime_types = validated_data.get('mime_type', None)
        topics = validated_data.get('topic', None)
        authors = validated_data.get('author', None)
        titles = validated_data.get('title', None)

        queryset = BooksBook.objects.all()

        if gutenberg_id:
            queryset = queryset.filter(gutenberg_id__in=gutenberg_id)
        
        if languages:
            queryset = queryset.filter(language__code__in=languages)

        if topics:
            topic_query = Q()
            for topic in topics:
                topic_query |= Q(bookshelf__name__icontains=topic)
                topic_query |= Q(subject__name__icontains=topic)
                
            queryset = queryset.filter(topic_query)

        if mime_types:
            formats_queryset = BooksFormat.objects.filter(mime_type__in=mime_types)
            queryset = queryset.prefetch_related(Prefetch('formats', queryset=formats_queryset))

        if authors:
            author_query = Q()
            for author in authors:
                author_query |= Q(authors__name__icontains=author)
            queryset = queryset.filter(author_query)

        if titles:
            title_query =Q()
            for title in titles:
                title_query |= Q(title__icontains=title)
            queryset = queryset.filter(title_query)

        queryset = queryset.distinct().order_by(F('download_count').desc(nulls_last=True))
        
        return queryset
