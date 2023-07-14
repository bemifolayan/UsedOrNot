import unittest
import sys

sys.path.append('../UsedOrNot')
from app import app  # imports flask app object

class Tests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_history_page(self):
        response = self.app.get('/history', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_liked_page(self):
        response = self.app.get('/liked', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def search(self, search):
        return self.app.post('/home',
                             data=dict(search=search),
                             follow_redirects=True)
    def test_valid_user_search(self):
        response = self.search('iphone')
        self.assertEqual(response.status_code, 200)
if __name__ == "__main__":
    unittest.main()