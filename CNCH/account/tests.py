from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SchoolGroup, Ticket


User = get_user_model()


class ProfileApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='organizer@example.com',
            email='organizer@example.com',
            password='safe-password',
            first_name='Ali',
            last_name='Ahmadi',
            phone_number='09120000001',
        )
        self.client.force_authenticate(self.user)

    def test_profile_registration_and_ticket_flow(self):
        group_response = self.client.post(reverse('group-create'), {
            'group_name': 'Brain Team',
            'province': 'Tehran',
            'city': 'Tehran',
            'school_name': 'Example School',
            'school_phone': '02112345678',
        })
        self.assertEqual(group_response.status_code, status.HTTP_201_CREATED)
        group = SchoolGroup.objects.get(pk=group_response.data['id'])
        self.assertEqual(group.organizer, self.user)

        student_response = self.client.post(reverse('student-create'), {
            'school_group': group.pk,
            'first_name': 'Sara',
            'last_name': 'Karimi',
            'national_id': '1234567890',
            'phone_number': '09120000002',
            'grade': 'دهم',
            'major': 'ریاضی',
        })
        self.assertEqual(student_response.status_code, status.HTTP_201_CREATED)

        ticket_response = self.client.post(reverse('profile-ticket-create'), {
            'title': 'Registration question',
            'message': 'Please check my registration.',
        })
        self.assertEqual(ticket_response.status_code, status.HTTP_201_CREATED)

        profile_response = self.client.get(reverse('profile'))
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['group']['id'], group.pk)
        self.assertEqual(len(profile_response.data['group']['students']), 1)
        self.assertEqual(len(profile_response.data['tickets']), 1)

    def test_email_update_keeps_email_login_username_in_sync(self):
        response = self.client.patch(reverse('profile'), {'email': 'new@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')
        self.assertEqual(self.user.username, 'new@example.com')

    def test_normal_user_cannot_open_admin_api(self):
        response = self.client.get(reverse('admin-user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_signup_account_can_obtain_a_jwt(self):
        self.client.force_authenticate(user=None)
        signup_response = self.client.post(reverse('signup'), {
            'email': 'new-user@example.com',
            'password': 'safe-password',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '09120000005',
        })
        self.assertEqual(signup_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(signup_response.data['role'], 'normal')

        token_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'new-user@example.com',
            'password': 'safe-password',
        })
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', token_response.data)


class AdminApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='safe-password',
            phone_number='09120000003',
            role='admin',
        )
        self.member = User.objects.create_user(
            username='member@example.com',
            email='member@example.com',
            password='safe-password',
            phone_number='09120000004',
        )
        self.ticket = Ticket.objects.create(user=self.member, title='Help', message='Need help')
        self.client.force_authenticate(self.admin)

    def test_admin_can_change_role_and_resolve_ticket(self):
        role_response = self.client.patch(
            reverse('admin-user-update', args=[self.member.pk]),
            {'role': 'mentor'},
        )
        self.assertEqual(role_response.status_code, status.HTTP_200_OK)
        self.member.refresh_from_db()
        self.assertEqual(self.member.role, 'mentor')

        ticket_response = self.client.post(
            reverse('admin-ticket-resolve', args=[self.ticket.pk]),
            {'resolved': True},
            format='json',
        )
        self.assertEqual(ticket_response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertTrue(self.ticket.resolved)
