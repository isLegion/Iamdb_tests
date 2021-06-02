from testhelpers import post_api, get_api, delete_api, put_api
import unittest
import logging

class TestMovie(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def setUp(self):
        self.new_movie = {'title': 'Inherent Vice', 'year': 2014}
        self.status_code, self.data = post_api('movies', self.new_movie)

    def test_1_post_movie_with_valid_data(self):
        assert self.status_code == 201
        assert self.data['title'] == self.new_movie['title']
        assert self.data['year'] == self.new_movie['year']
        assert isinstance(self.data['id'], str)

    def test_2_get_movie_with_valid_data(self):
        status_code, data_get = get_api('movies', self.data['id'])
        assert status_code == 200
        assert self.data['title'] == self.new_movie['title']
        assert self.data['year'] == self.new_movie['year']

    def test_3_put_movie_with_valid_data(self):
        self.data['year'] = 2021
        status_code, data_put = put_api('movies', self.data['id'], self.data)
        assert status_code == 200
        assert data_put['title'] == self.new_movie['title']
        assert data_put['year'] == 2021

    def test_4_delete_movie_with_valid_data(self):
        status_code, data_deleted = delete_api('movies', self.data['id'])
        assert status_code == 200
        assert data_deleted == 'Movie successfully deleted'
        status_code_get, data_get = get_api('movies', self.data['id'])
        assert status_code_get == 404
        assert data_get == 'No movies found'

    def test_5_post_movie_with_invalid_data(self):
        invalid_movie = {'title': 'Under silver lake'}
        status_code, data = post_api('movies', invalid_movie)
        assert status_code == 400
        assert data == 'Missing required field year'

    def test_7_put_get_movie_with_invalid_data(self):
        self.data['year'] = 2222
        status_code, data_put = put_api('movies', 'notExistingId', self.data)
        assert status_code == 201
        status_code_get, data_get = get_api('movies', 'notExistingId')
        assert status_code_get == 404
        assert data_get == 'No movies found'

    def test_8_delete_movie_with_invalid_data(self):
        status_code, data_deleted = delete_api('movies', 'notExistingId')
        assert status_code == 404
        assert data_deleted == 'Movie not found'


