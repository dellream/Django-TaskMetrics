from django.test import TestCase


class HomePageTest(TestCase):
    def test_home_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
