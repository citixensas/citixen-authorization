import unittest

from corexen.utils.shortcuts import CitixenChoices


class ShortCutsTest(unittest.TestCase):

    def test_convert_enum_to_tuple(self):
        class Test(CitixenChoices):
            OPTION1 = (1, 'Opcion 1')
            OPTION2 = (2, 'Opcion 2')
        result = Test.choices()
        self.assertEqual(result, ((1, 'Opcion 1'), (2, 'Opcion 2')))
        self.assertEqual(Test.OPTION1, 1)
        self.assertEqual(Test.OPTION2, 2)

    def test_convert_enum_to_tuple_with_ignored_fields(self):
        class Test(CitixenChoices):
            OPTION1 = (1, 'Opcion 1', False)
            OPTION2 = (2, 'Opcion 2')
        result = Test.choices()
        self.assertEqual(result, ((2, 'Opcion 2'),))
        self.assertEqual(Test.OPTION1, 1)
        self.assertEqual(Test.OPTION2, 2)
