import json
import random

from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from ..constants import TicketStatus
from kanban.board.models import Ticket
from kanban.board.tests.factories import TicketFactory


class TicketTests(TestCase):
    def test_post(self):
        fake = Faker()
        url = reverse('ticket-list')
        data = {
            'assignee': None,
            'name': fake.word(),
            'description': fake.text(),
            'status': random.choice([x.value for x in TicketStatus]),
            'start': str(fake.date_object()),
            'end': None,
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().name, data['name'])

    def test_get(self):
        ticket = TicketFactory()
        url = reverse('ticket-detail', kwargs={'pk': ticket.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': ticket.id,
            'assignee': ticket.assignee.username,
            'status_display': ticket.get_status_display(),
            'name': ticket.name,
            'description': ticket.description,
            'status': ticket.status,
            'start': ticket.start,
            'end': ticket.end,
        })