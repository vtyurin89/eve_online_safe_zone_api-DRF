import unittest
from unittest.mock import patch, MagicMock

from ..tasks import UpdateStarDb
from ..models import DangerRating


class TestUpdateStarDb(unittest.TestCase):
    def setUp(self):
        self.update_star_db = UpdateStarDb()

    @patch('requests.get')
    def test_process_system_kills(self, mock_get):
        # Modelling API response
        mock_get.return_value.json.return_value = [
            {'system_id': 1, 'npc_kills': 10, 'pod_kills': 5, 'ship_kills': 20},
            {'system_id': 2, 'npc_kills': 5, 'pod_kills': 2, 'ship_kills': 15},
        ]

        self.update_star_db._process_system_kills()

        # testing system_data's correctness
        self.assertEqual(self.update_star_db.system_data, {
            1: {'npc_kills': 10, 'pod_kills': 5, 'ship_kills': 20},
            2: {'npc_kills': 5, 'pod_kills': 2, 'ship_kills': 15},
        })

    @patch('requests.get')
    def test_process_system_jumps(self, mock_get):
        self.update_star_db.system_data = {
            1: {'npc_kills': 10, 'pod_kills': 5, 'ship_kills': 20},
            2: {'npc_kills': 5, 'pod_kills': 2, 'ship_kills': 15},
        }

        # Modelling API response
        mock_get.return_value.json.return_value = [
            {'system_id': 1, 'ship_jumps': 30},
            {'system_id': 3, 'ship_jumps': 10},
        ]

        self.update_star_db._process_system_jumps()

        # testing system_data's correctness
        self.assertEqual(self.update_star_db.system_data, {
            1: {'npc_kills': 10, 'pod_kills': 5, 'ship_kills': 20, 'ship_jumps': 30},
            2: {'npc_kills': 5, 'pod_kills': 2, 'ship_kills': 15},
            3: {'ship_jumps': 10},
        })

    def test_calculate_rating(self):
        self.update_star_db.system_data = {
            1: {'npc_kills': 10, 'pod_kills': 5, 'ship_kills': 20, 'ship_jumps': 30},
            2: {'npc_kills': 5, 'pod_kills': 2, 'ship_kills': 15},
            3: {'ship_jumps': 10},
        }

        self.update_star_db._calculate_rating()

        # checking system_data
        self.assertEqual(self.update_star_db.system_data, {
            1: {'npc_kills': 10, 'pod_kills': 5, 'ship_kills': 20, 'ship_jumps': 30, 'rating_change': 5040},
            2: {'npc_kills': 5, 'pod_kills': 2, 'ship_kills': 15, 'rating_change': 3405},
            3: {'ship_jumps': 10, 'rating_change': 10},
        })


if __name__ == '__main__':
    unittest.main()

