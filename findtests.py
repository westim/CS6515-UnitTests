import unittest
import sys
import random
import math
import time
from findX import findXinA
from GA_ProjectUtils import ExceededLookupsError, findX

class TestFindX(unittest.TestCase):
    """
    Unit tests for CS6515, Coding Project 2: Find x in Infinite Array, Spring 2022.

    Author: Tim West (timwest@gatech.edu)

    This suite contains several different types of tests:

      1. Repeated Elements

        This test suite is designed to ensure that the implementation
        does not rely on the assumption of unique elements. This invalid assumption
        is currently baked into the provided `findX` class which populates input
        A using `random.sample()`, which samples without replacement.

        The assignment FAQ states that the elements cannot be assumed to be unique,
        despite the current implementation for `findX`.

      2. Random Tests

        In effort to cover as many possibilities as possible, this suite
        runs 100 tests with random bounds as well as 100 tests with
        the default bounds (10, 100000).

      3. Known Tests

        These 14 tests were created by classmates with known seeds & expected indices.

      4. None Tests

        These 2 tests check for values of x which are not expected in A.
    """
    def setUp(self):
        self.findXStatic = findXStatic()
        self.findX = findX()

    def test_repeat(self):
        """Find one of the valid indices for 2."""
        idx, n = findXinA(3, self.findXStatic)
        self.assertIn(idx, [2, 3])
        self.assertLessEqual(n, self.findXStatic._findXStatic__maxCalls)

    def test_repeat_2(self):
        """Find the index of 4, which appears after repeated values."""
        idx, n = findXinA(4, self.findXStatic)
        self.assertEqual(idx, 4)
        self.assertLessEqual(n, self.findXStatic._findXStatic__maxCalls)

    def test_repeat_none(self):
        """Value 6 is not in A."""
        idx, n = findXinA(6, self.findXStatic)
        self.assertEqual(idx, None)
        self.assertLessEqual(n, self.findXStatic._findXStatic__maxCalls)

    def test_repeat_lesser(self):
        """Value 1 is not in A and < A[1]."""
        idx, n = findXinA(1, self.findXStatic)
        self.assertEqual(idx, None)
        self.assertLessEqual(n, self.findXStatic._findXStatic__maxCalls)

    def test_repeat_none_greater(self):
        """Value 1001 is not in A and > A[n]."""
        idx, n = findXinA(1001, self.findXStatic)
        self.assertEqual(idx, None)
        self.assertLessEqual(n, self.findXStatic._findXStatic__maxCalls)

    def test_random_max_calls(self):
        """Tests 100 random ranges for the Max Call limit."""
        diff = []
        for _ in range(random_trials):
            lower = random.choice(range(1, 100))
            upper = random.choice(range(lower+1, 100_000))
            seed = int(time.time()*1000)
            x = self.findX.start(seed, lower, upper)
            theIndex, numLookups = findXinA(x, self.findX)
            isNotPresent = x not in self.findX._findX__A[1:] # Ignore A[0]
            if isNotPresent:
                self.assertEqual(None, theIndex, f'Expected index None. seed={seed}, nLower={lower}, nUpper={upper}')
            else:
                self.assertEqual(self.findX._findX__A[theIndex], x, f'Expected to find value {x}. seed={seed}, nLower={lower}, nUpper={upper}')
            self.assertLessEqual(numLookups, self.findX._findX__maxCalls, f'Used {numLookups} lookups, maximum={self.findX._findX__maxCalls}. seed={seed}, nLower={lower}, nUpper={upper}')
            diff.append(self.findX._findX__maxCalls - numLookups)
        print(f'Minimum remaining calls: {min(diff)}, Average remaining calls: {sum(diff) / len(diff)}')

    def test_seeds(self):
        """Tests the first 100 random number seeds for default bounds."""
        for seed in range(random_trials):
            x = self.findX.start(seed)
            theIndex, numLookups = findXinA(x, self.findX)
            isNotPresent = x not in self.findX._findX__A[1:] # Ignore A[0]
            if isNotPresent:
                self.assertEqual(None, theIndex, f'Expected index None. seed={seed}')
            else:
                self.assertEqual(self.findX._findX__A[theIndex], x, f'Expected to find value {x}. seed={seed}')
            self.assertLessEqual(numLookups, self.findX._findX__maxCalls, f'Used {numLookups} lookups, maximum={self.findX._findX__maxCalls}. seed={seed}')

    def test_gerardo(self):
        """Tests orginally created by Gerardo (gnevarez@gatech.edu)"""
        seeds = [123456, 12, 123, 1234, 5, 55555, 1234567890, 0, 1, 2, 3, 3683055014, 31,700003]
        indices = [10759, 50220, 923, 41939, 15580, 2267, 31815, 21848, 2980, 6096,7840, 4700, 1237, 124]
        for seed, idx in zip(seeds, indices):
            x = self.findX.start(seed)
            index, calls = findXinA(x, self.findX)
            self.assertEqual(index, idx, f'Error on seed {seed}, expected index {idx}, got {index}')
            print(f'Seed {seed}: x found at index {index} in {calls} calls')

    def test_none(self):
        """Tests originally created by Dan Driscoll"""
        self.findX.start(1)
        index, calls = findXinA(29, self.findX)
        self.assertEqual(index, None, f'Failed x below findX.lookup(1), returned {index} instead of None')
        
        index, calls = findXinA(57, self.findX)
        self.assertEqual(index, None, f'Failed x between findX.lookup(1) & findX.lookup(2), returned {index} instead of None')

class findXStatic():
    """Hardcoded test class with repeated elements."""
    def __init__(self):
        # A[0] should never be accessed
        self.__A = [None, 2, 3, 3, 4, 5, 1000]
        self.__n = 6
        self.__lookupCount = 0
        self.__maxCalls = int(math.log(self.__n, 2)*2) + 2
        return

    def lookup(self, i):
        self.__lookupCount += 1
        
        if self.__lookupCount > self.__maxCalls:
            raise ExceededLookupsError('Exceeded Maximum of {} Lookups'.format(self.__maxCalls))
        if i > self.__n:
            return None
        else:
            return self.__A[i]
    
    def lookups(self):
        return self.__lookupCount


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[1]])
    random_trials = sys.argv[1] if sys.argv[1] is not None else 100
