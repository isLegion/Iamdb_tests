from testhelpers import post_api, get_api, delete_api, put_api, get_all_api
import unittest

class TestSearch(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.status_code, self.data = get_all_api('persons')
        assert self.status_code == 200
        for key in self.data:
            status_code, data = delete_api('persons', key['id'])
            assert status_code == 200
        self.status_code, self.data = get_all_api('movies')
        assert self.status_code == 200
        for key in self.data:
            status_code, data = delete_api('movies', key['id'])
            assert status_code == 200
        self.new_person = {'first_name': 'Joaquin', 'last_name': 'Phoenix', 'birth_year': 1976}
        self.new_movie = {'title': 'Inherent Vice', 'year': 2014}
        self.new_person_2 = {'first_name': 'Andrew', 'last_name': 'Garfield', 'birth_year': 1983}
        self.new_movie_2 = {'title': 'Under the Silver Lake', 'year': 2014}
        self.status_code_person, self.data_person = post_api('persons', self.new_person)
        self.status_code_movie, self.data_movie = post_api('movies', self.new_movie)
        assert self.status_code_person == 201
        assert self.status_code_movie == 201
        self.status_code_person_2, self.data_person_2 = post_api('persons', self.new_person_2)
        self.status_code_movie_2, self.data_movie_2 = post_api('movies', self.new_movie_2)
        assert self.status_code_person_2 == 201
        assert self.status_code_movie_2 == 201

    def test_1_search_valid_name_title(self):
        query = 'Joaquin-Inherent'
        status_code_search, data_search = get_api('search', query)
        assert status_code_search == 200
        assert len(data_search) == 2
        assert data_search[0]['id'] == self.data_person['id']
        assert data_search[1]['id'] == self.data_movie['id']

    def test_2_search_valid_last_name_year(self):
        query = 'Phoenix-2014'
        status_code_search, data_search = get_api('search', query)
        assert status_code_search == 200
        assert len(data_search) == 1
        assert data_search[0]['id'] == self.data_person['id']

    def test_3_search_valid_name_last_name_title(self):
        query = 'Phoenix-Andrew-lake'
        status_code_search, data_search = get_api('search', query)
        assert status_code_search == 200
        assert len(data_search) == 3
        assert data_search[0]['id'] == self.data_person['id']
        assert data_search[1]['id'] == self.data_person_2['id']
        assert data_search[2]['id'] == self.data_movie_2['id']

    def test_4_search_valid_name_last_name_same_person(self):
        query = 'Phoenix-Joaquin'
        status_code_search, data_search = get_api('search', query)
        assert status_code_search == 200
        assert len(data_search) == 2
        assert data_search[0]['id'] == self.data_person['id']
        assert data_search[1]['id'] == self.data_person['id']

    def test_5_search_invalid_data(self):
        query = 'Francis-Ford-Coppola'
        status_code_search, data_search = get_api('search', query)
        assert status_code_search == 404
        assert data_search == 'No results'






