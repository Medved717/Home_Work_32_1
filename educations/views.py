from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from educations.models import Course, Lesson
from educations.paginators import CoursePaginations, LessonPaginations
from educations.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginations

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAdminUser,)
        elif self.action == 'update':
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == 'list':
            self.permission_classes = (IsModer | IsAdminUser,)
        elif self.action == 'destroy':
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_lesson = LessonPaginations


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdminUser | IsAuthenticated & ~IsModer)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsAdminUser | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsAdminUser | IsOwner,)


class LessonDestroyAPIViews(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAdminUser | IsOwner,)
    serializer_class = LessonSerializer
