from unittest import TestCase

from hms_base.decorators import singleTopicListener

class TestSingleTopicListener(TestCase):
    def setUp(self):
        @singleTopicListener('bla')
        def listener(client, topic, dct):
            return 42

        self.listener = listener

    def test_accept(self):
        self.assertEqual(42, self.listener(None, 'bla', {'test': True}))

    def test_reject(self):
        self.assertEqual(None, self.listener(None, 'truc', {'test': True}))