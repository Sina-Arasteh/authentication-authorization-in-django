from django.test import TestCase, Client


class IndexPageTests(TestCase):
    def setUp(self):
        self.c = Client()

    def test_render(self):
        response = self.c.get("")
        self.assertTemplateUsed(response, 'accounts/index.html')
