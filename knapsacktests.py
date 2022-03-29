import unittest
from knapsack import knapsack

class TestKnapsack(unittest.TestCase):
    '''
    Unit tests for CS6515, Coding Project 1: Knapsack, Spring 2022.

    Author: Tim West (timwest@gatech.edu)

    This resource is unofficial and not guaranteed to be
    comprehensive or correct. Please use at your own risk.
    '''
    def test_none(self):
        '''None of the available items satisfy w <= B.'''
        self.assertEqual(knapsack({1: ('x', 2, 1)}, 1), [], 'This is not a required case, per assignment instructions.')

    def test_simple(self):
        '''One item available where w == B.'''
        self.assertEqual(knapsack({1: ('x', 1, 1)}, 1), [('x', 1, 1)], 'Expected the only available item.')

    def test_all(self):
        '''Sum of all item weights == B.'''
        ans = sorted(knapsack({1: ('x', 1, 1), 2: ('y', 3, 1)}, 4))
        self.assertEqual(ans, [('x', 1, 1), ('y', 3, 1)], 'Expected all items where sum(w[i]) == B.')

    def test_take_fit(self):
        '''Take the only item where w <= B.'''
        ans = knapsack({1: ('x', 20, 1), 2: ('y', 30, 1)}, 25)
        self.assertEqual(ans, [('x', 20, 1)], 'Expected only the item with w <= B.')

    def test_take_high_value_low_weight(self):
        '''Take only the item with the higher value & lower weight.'''
        ans = knapsack({1: ('x', 5, 10), 2: ('y', 1, 20)}, 5)
        self.assertEqual(ans, [('y', 1, 20)], 'Expected only the item with higher value & lower weight.')

    def test_take_high_value_high_weight(self):
        '''Take only the item with the higher value & higher weight.'''
        ans = knapsack({1: ('x', 1, 10), 2: ('y', 5, 20)}, 5)
        self.assertEqual(ans, [('y', 5, 20)], 'Expected only the item with higher value & higher weight.')

    def test_not_greedy(self):
        '''Don't take greedy approach (highest value first).'''
        ans = sorted(knapsack({1: ('x', 1, 10), 2: ('y', 5, 20), 3: ('z', 4, 15)}, 5))
        self.assertEqual(ans, [('x', 1, 10), ('z', 4, 15)], 'Expected the non-greedy algorithm.')

    def test_any_one(self):
        '''Take any one of the best, equivalent solutions.'''
        ans = knapsack({1: ('x', 5, 10), 2: ('y', 5, 10)}, 5)
        self.assertIn(ans, [[('x', 5, 10)], [('y', 5, 10)]], 'Expected one item.')
        self.assertNotEqual(ans, [('x', 5, 10), ('y', 5, 10)], 'Expected not both items for tied solutions.')

    def test_increasing_all(self):
        '''Take all items when ordered by increasing weight & value.'''
        ans = sorted(knapsack({1: ('w', 1, 1), 2: ('x', 2, 2), 3: ('y', 3, 3), 4: ('z', 4, 4)}, 10))
        self.assertEqual(ans, [('w', 1, 1), ('x', 2, 2), ('y', 3, 3), ('z', 4, 4)])

    def test_increasing(self):
        '''Take all but the first item when ordered by increasing weight & value.'''
        ans = sorted(knapsack({1: ('w', 1, 1), 2: ('x', 2, 2), 3: ('y', 3, 3), 4: ('z', 4, 4)}, 9))
        self.assertEqual(ans, [('x', 2, 2), ('y', 3, 3), ('z', 4, 4)])

    def test_decreasing_all(self):
        '''Take all items when ordered by decreasing weight & value.'''
        ans = sorted(knapsack({1: ('w', 4, 4), 2: ('x', 3, 3), 3: ('y', 2, 2), 4: ('z', 1, 1)}, 10))
        self.assertEqual(ans, [('w', 4, 4), ('x', 3, 3), ('y', 2, 2), ('z', 1, 1)])

    def test_decreasing(self):
        '''Take all but the last item when ordered by decreasing weight & value.'''
        ans = sorted(knapsack({1: ('w', 4, 4), 2: ('x', 3, 3), 3: ('y', 2, 2), 4: ('z', 1, 1)}, 9))
        self.assertEqual(ans, [('w', 4, 4), ('x', 3, 3), ('y', 2, 2)])

    def test_val_increase_weight_decrease_all(self):
        '''Take all items when ordered by decreasing weight & increasing value.'''
        ans = sorted(knapsack({1: ('w', 4, 1), 2: ('x', 3, 2), 3: ('y', 2, 3), 4: ('z', 1, 4)}, 10))
        self.assertEqual(ans, [('w', 4, 1), ('x', 3, 2), ('y', 2, 3), ('z', 1, 4)])

    def test_val_increase_weight_decrease(self):
        '''Take all but the lowest-value item when ordered by decreasing weight & increasing value.'''
        ans = sorted(knapsack({1: ('w', 4, 1), 2: ('x', 3, 2), 3: ('y', 2, 3), 4: ('z', 1, 4)}, 9))
        self.assertEqual(ans, [('x', 3, 2), ('y', 2, 3), ('z', 1, 4)])
        
    def test_val_decrease_weight_increase_all(self):
        '''Take all items when ordered by increasing weight & decreasing value.'''
        ans = sorted(knapsack({1: ('w', 1, 4), 2: ('x', 2, 3), 3: ('y', 3, 2), 4: ('z', 4, 1)}, 10))
        self.assertEqual(ans, [('w', 1, 4), ('x', 2, 3), ('y', 3, 2), ('z', 4, 1)])

    def test_val_decrease_weight_increase(self):
        '''Take all but the lowest-value item when ordered by increasing weight & decreasing value.'''
        ans = sorted(knapsack({1: ('w', 1, 4), 2: ('x', 2, 3), 3: ('y', 3, 2), 4: ('z', 4, 1)}, 9))
        self.assertEqual(ans, [('w', 1, 4), ('x', 2, 3), ('y', 3, 2)])

if __name__ == '__main__':
    unittest.main()
