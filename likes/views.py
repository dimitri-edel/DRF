from rest_framework import generics, permissions
from DRF_prj.permissions import IsOwnerOrReadOnly
from likes.models import Likes
from likes.serializers import LikesSerializer

class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikesSerializer
    queryset = Likes.objects.all()
