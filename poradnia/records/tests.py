from django.test import TestCase
from letters.factories import LetterFactory
from records.models import Record


class RecordTestCase(TestCase):
    def test_content_object(self):
        letter = LetterFactory()
        obj = Record()
        obj.content_object = letter
        self.assertEqual(obj.content_object, letter)
        self.assertEqual(obj.letter, letter)
        self.assertEqual(obj.object_id, letter.pk)
