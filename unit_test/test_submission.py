from django.test import TestCase

from problem.models import Problem
from support.models import Language
from submission.serializers import SubmissionSerializer


# Create your tests here.

class SerializerTest(TestCase):
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        self.user = 'unit_test_user'

    def setUp(self):
        Language.objects.filter(oj_name='unit_test_oj', oj_language='unit_test_language',
                                oj_language_name='unit_test_language_name').delete()
        Problem.objects.filter(remote_oj='unit_test_oj', remote_id='unit_test_pid').delete()
        Language.objects.create(oj_name='unit_test_oj', oj_language='unit_test_language',
                                oj_language_name='unit_test_language_name').save()
        Problem.objects.create(remote_oj='unit_test_oj', remote_id='unit_test_pid').save()

    def tearDown(self):
        Language.objects.filter(oj_name='unit_test_oj', oj_language='unit_test_language',
                                oj_language_name='unit_test_language_name').delete()
        Problem.objects.filter(remote_oj='unit_test_oj', remote_id='unit_test_pid').delete()

    def test_submission_1(self):
        request_data = {
            "remote_oj": "unit_test_oj",
            "remote_id": "unit_test_pid",
            "code": "#include <cstdio>"
                    "#include <cstring>"
                    "#include <algorithm>"
                    ""
                    "using namespace std;"
                    "int main(int argc, char **argv){"
                    ""
                    "   std::cout << \"Hello World\" << std::endl;"
                    "}",
            "language": "unit_test_language"
        }

        serializer = SubmissionSerializer(data=request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_submission_2(self):
        request_data = {
            "remote_oj": "unit_test_oj",
            "remote_id": "unit_test_pid",
            "code": "#include <cstdio>"
                    "#include <cstring>"
                    "#include <algorithm>"
                    ""
                    "using namespace std;"
                    "int main(int argc, char **argv){"
                    ""
                    "   std::cout << \"Hello World\" << std::endl;"
                    "}",
            "language": "unit_test_language"
        }

        serializer = SubmissionSerializer(data=request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_submission_3(self):
        request_data = {
            "remote_oj": "unit_test_oj",
            "remote_id": "unit_test_pid",
            "code": "",
            "language": "unit_test_language"
        }

        serializer = SubmissionSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_submission_4(self):
        request_data = {
            "remote_oj": "unit_test_oj",
            "remote_id": "unit_test_pid",
            "language": "unit_test_language"
        }

        serializer = SubmissionSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
