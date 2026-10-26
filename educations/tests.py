from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from educations.models import Course
from users.models import User


class CourseTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.course_python = Course.objects.create(title='Python разработчик', description='Курс по изучению языка программирования python.')
        self.course_C = Course.objects.create(title='C++ разработчик',
                                                   description='Курс по изучению языка программирования C++.')

    def test_create_course(self):
        url = reverse('educations:courses-list')
        data = {
            'title': 'java разработчик',
            'description': 'Курс по изучению языка программирования java.'
        }
        response = self.client.post(url, data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.get(title='java разработчик').title, 'java разработчик')

    def test_list_course(self):
        url = reverse('educations:courses-list')
        response = self.client.get(url)
        self.assertEqual(response.data.get('count'), 2)

    def test_retrieve_course(self):
        url = reverse('educations:courses-detail', args=(self.course_python.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'Python разработчик')

    def test_update_course(self):
        url = reverse('educations:courses-detail', args=(self.course_C.pk,))
        data = {'title': 'Изменение'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'Изменение')

    def test_delete_course(self):
        url = reverse('educations:courses-detail', args=(self.course_C.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(Course.objects.get(title='Python разработчик').title, 'Python разработчик')