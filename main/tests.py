from django.test import TestCase, Client
from main.models import Item

# Create your tests here.

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/main/')
        self.assertTemplateUsed(response, 'main.html')
        
class ItemTestCase(TestCase):
    def setUp(self):
        Item.objects.create(
            name= 'The Art of War',
            amount= 1,
            description= 'The ancient Chinese military text, dating from the Late Spring and Autumn Period, was written by Sun Tzu.'
        )

    def test_item_detail_is_correct(self):
        ArtOfWar = Item.objects.get(name='The Art of War')
        self.assertEqual(ArtOfWar.amount, 1)
        self.assertEqual(ArtOfWar.description, 'The ancient Chinese military text, dating from the Late Spring and Autumn Period, was written by Sun Tzu.') 