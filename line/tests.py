from django.test import TestCase
from unittest import mock
from line.line_service import Line
from line.views import LineHookView
# Create your tests here.

def mock_line_get_token():
    result = {
        'ok': True,
        'result': {
            'userId': 'test1'
        }
    }
    return result


class Test(TestCase):
    
    def setUp(self):
        self.line = Line()
    
    @mock.patch('line.line_service.Line.get_token', side_effect=mock_line_get_token)
    def test_line_hook_bussiness_logic(self, *args):
        instance = LineHookView()
        code = 'test'
        branch_id = 1
        user_id, state = instance.businesslogic(code, branch_id)
        self.assertTrue(state)
        self.assertEqual(user_id, 'test1')