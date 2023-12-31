from rest_framework import status
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics, filters #, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from DRF_prj.permissions import IsOwnerOrReadOnly
from django.http import Http404
from django.db.models import Count


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # annotate will add computed fields to the list
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count = Count('likes', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # fields for SearchFilter
    search_fields = [
        'owner__username',
        'title'
    ]
    # fields for OrderingFilter
    ordering_fields = [
        'comments_count',        
        'likes_count',
        'likes__created_at',
    ]
    # fields for DjangoFilterBackend
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count = Count('comment', distinct=True),
        likes_count = Count('likes', distinct=True)
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter
    ]

    ordering_fields = [
        'comments_count',        
        'likes_count',
        'likes__created_at',
    ]
    
# class PostList(APIView):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(
#             posts, many=True, context={'request': request}
#         )
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(
#             data=request.data, context={'request': request}
#         )

#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     # Attribute of APIView that creates a form for the object
#     serializer_class = PostSerializer
#     # Attribute of APIView that allows to manage permissions
#     permission_classes = [IsOwnerOrReadOnly]

#     def get_object(self, pk):
#     # retrieve the object from the database
#         try:
#             post = Post.objects.get(pk=pk)
#              # Call an method of APIView to check the permissions
#             # If the user does not have permission, the method will
#             # thrwo the 403 Error (Forbidden)
#             self.check_object_permissions(self.request, post)
#             return post
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, context={"request": request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data, context={"request": request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)