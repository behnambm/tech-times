from . import BaseTestCase


class ViewsTestCase(BaseTestCase):
    def test_home_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000')
        self.assertEqual(response.status_code, 200)

    def test_home_context(self):
        response = self.client.get('http://127.0.0.1:8000')
        articles = response.context_data['object_list']
        self.assertEqual(articles[0].title, 'Test Article 11')
