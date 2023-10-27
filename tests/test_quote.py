import unittest
from flask_testing import TestCase
from app import app, db, UserCredentials

class TestQuoteRoute(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        return app

    def setUp(self):
        self.client.post('/sign_up', data=dict(username='testuser',
                                               password='testpassword'), follow_redirects=True)

        self.client.post('/login', data=dict(username='testuser',
                                             password='testpassword'), follow_redirects=True)
        
        self.client.post('/profile', data=dict(fullName='testuser',
                                                        addressOne='123 St',
                                                        addressTwo='345 Dr',
                                                        city='Houston',
                                                        state='TX',
                                                        zipcode='77092'), follow_redirects=True)
        
        self.client.post('/quote', data=dict(gallons=100,
                                             deliveryDate='2023-11-01'), follow_redirects=True)

    def tearDown(self):
        self.client.get('/logout', follow_redirects=True)
        
        test_user = UserCredentials.query.filter_by(username='testuser').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()

    def test_quote_access(self):
        response = self.client.get('/quote', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()