from django.test import TestCase


class StaticFilesTestCase(TestCase):
    def test_admin_stylesheet_is_served(self):
        response = self.client.get('/static/admin/assets/css/style.css')
        self.assertEqual(response.status_code, 200)
