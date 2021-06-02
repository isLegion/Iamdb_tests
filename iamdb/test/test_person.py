from testhelpers import post_api, get_api, delete_api, put_api, get_all_api
import unittest
import logging

class TestPerson(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def setUp(self):
        self.new_person = {'first_name': 'Patrick', 'last_name': 'Stewart', 'birth_year': 1940}
        self.status_code, self.data = post_api('persons', self.new_person)

    def test_1_post_person_with_valid_data(self):
        assert self.status_code == 201
        assert self.data['first_name'] == self.new_person['first_name']
        assert self.data['last_name'] == self.new_person['last_name']
        assert self.data['birth_year'] == self.new_person['birth_year']
        assert isinstance(self.data['id'], str)

    def test_2_get_person_with_valid_data(self):
        status_code, data_get = get_api('persons', self.data['id'])
        assert status_code == 200
        assert self.data['first_name'] == self.new_person['first_name']
        assert self.data['last_name'] == self.new_person['last_name']
        assert self.data['birth_year'] == self.new_person['birth_year']

    def test_3_put_person_with_valid_data(self):
        self.data['birth_year'] = 1991
        status_code, data_put = put_api('persons', self.data['id'], self.data)
        assert status_code == 200
        assert data_put['first_name'] == self.new_person['first_name']
        assert data_put['last_name'] == self.new_person['last_name']
        assert data_put['birth_year'] == 1991

    def test_4_delete_person_with_valid_data(self):
        status_code, data_deleted = delete_api('persons', self.data['id'])
        assert status_code == 200
        assert data_deleted == 'Person successfully deleted'
        status_code_get, data_get = get_api('persons', self.data['id'])
        assert status_code_get == 404
        assert data_get == 'No persons found'

    def test_5_post_person_with_invalid_data(self):
        invalid_person = {'first_name': 'Patrick', 'last_name': 'Stewart'}
        status_code, data = post_api('persons', invalid_person)
        assert status_code == 400
        assert data == 'Missing required field birth_year'

    def test_7_put_get_person_with_invalid_data(self):
        self.data['birth_year'] = 1991
        status_code, data_put = put_api('persons', 'notExistingId', self.data)
        assert status_code == 201
        status_code_get, data_get = get_api('persons', 'notExistingId')
        assert status_code_get == 404
        assert data_get == 'No persons found'

    def test_8_delete_person_with_invalid_data(self):
        status_code, data_deleted = delete_api('persons', 'notExistingId')
        assert status_code == 404
        assert data_deleted == 'Person not found'

    @classmethod
    def tearDownClass(self):
        self.status_code, self.data = get_all_api('persons')
        assert self.status_code == 200
        for key in self.data:
            status_code, data = delete_api('persons', key['id'])
            assert status_code == 200

