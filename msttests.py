import GA_ProjectUtils as utils
import mst

import unittest
from itertools import permutations
from collections import Counter


class MstTest(unittest.TestCase):
    """
    Unit tests for CS6515, Coding Project 3: MST, Spring 2022.

    Author: Tim West (timwest@gatech.edu)

    This resource is unofficial and not guaranteed to be
    comprehensive or correct. Please use at your own risk.
    """

    def verifyConnected(self, uf):
        """
        Helper to verify MST is fully connected.
        This will also test the implementation of `areConnected()`.
        """
        num_vertices = len(uf.rank)
        for u, v in permutations(range(num_vertices), 2):
            self.assertTrue(uf.areConnected(u, v), f"Nodes {u} and {v} are not connected; check your output and/or `areConnected()`.")

    def verifyUnionFindProps(self, uf):
        self.verifyProp1(uf)
        self.verifyProp3(uf)

    def verifyProp1(self, uf):
        """Verifies Property 1 of Union-Find."""
        for x in range(len(uf.rank)):
            if x != uf.pi[x]:
                self.assertTrue(uf.rank[x] < uf.rank[uf.pi[x]])

    def verifyProp3(self, uf):
        """Verifies Property 3 of Union-Find."""
        n = len(uf.rank)
        count_dict = Counter(uf.rank)
        for k, count in count_dict.items():
            self.assertTrue(count <= n/2**k)

    def test_simple(self):
        """Tests with 2 vertices & 1 edge."""
        G = utils.Graph(2, [[1, 0, 1]])
        MST, uf = mst.kruskal(G)
        self.assertEqual(len(MST), 1)
        self.assertEqual(utils.findTotalWeightOfMst(MST), 1)
        self.assertTrue(uf.areConnected(0, 1))

    def test_cycle_lower(self):
        """Tests that the heaviest edge is not taken in the cycle."""
        G = utils.Graph(3, [[1, 0, 1], [1, 1, 2], [2, 2, 0]])
        MST, uf = mst.kruskal(G)
        self.assertEqual(len(MST), 2)
        self.assertEqual(utils.findTotalWeightOfMst(MST), 2)
        self.verifyConnected(uf)
        self.verifyUnionFindProps(uf)

    def test_take_heaviest(self):
        """Tests that the heaviest edge must be taken."""
        G = utils.Graph(4, [[1, 0, 1], [1, 1, 2], [3, 2, 3]])
        MST, uf = mst.kruskal(G)
        self.assertEqual(len(MST), 3)
        self.assertEqual(utils.findTotalWeightOfMst(MST), 5)
        self.verifyConnected(uf)
        self.verifyUnionFindProps(uf)

    def test_take_any(self):
        """Tests any 2 of 3 edges are taken."""
        G = utils.Graph(3, [[1, 0, 1], [1, 1, 2], [1, 2, 0]])
        MST, uf = mst.kruskal(G)
        self.assertEqual(len(MST), 2)
        self.assertEqual(utils.findTotalWeightOfMst(MST), 2)
        self.verifyConnected(uf)
        self.verifyUnionFindProps(uf)

    def test_5_1(self):
        """Tests DPV Exercise 5.1."""
        G = utils.Graph(8, [
            [6, 0, 1],
            [5, 1, 2],
            [6, 2, 3],
            [1, 0, 4],
            [2, 1, 4],
            [2, 1, 5],
            [1, 5, 4],
            [5, 2, 5],
            [4, 2, 6],
            [3, 6, 5],
            [5, 3, 6],
            [7, 3, 7],
            [3, 7, 6]
        ])
        MST, uf = mst.kruskal(G)
        self.assertEqual(len(MST), 7)
        self.assertEqual(utils.findTotalWeightOfMst(MST), 19)
        self.verifyConnected(uf)
        self.verifyUnionFindProps(uf)

    def test_5_2(self):
        """Tests DPV Exercise 5.2."""
        G = utils.Graph(8, [
            [1, 0, 1],
            [2, 1, 2],
            [3, 2, 3],
            [4, 0, 4],
            [8, 0, 5],
            [5, 4, 5],
            [6, 1, 5],
            [6, 1, 6],
            [1, 5, 6],
            [2, 2, 6],
            [1, 3, 6],
            [1, 7, 6],
            [4, 3, 7]
        ])
        MST, uf = mst.kruskal(G)
        self.assertEqual(len(MST), 7)
        self.assertEqual(utils.findTotalWeightOfMst(MST), 12)
        self.verifyConnected(uf)
        self.verifyUnionFindProps(uf)

    def test_find(self):
        """
        Test from DPV Figure 5.7 by Foster Gorman.
        This checks for path compression behavior.
        """
        uf = mst.unionFind(11)
        #          0  1  2  3  4  5  6  7  8  9  10
        #          A  B  C  D  E  F  G  H  I  J  K
        uf.pi = [0, 0, 0, 2, 0, 4, 4, 4, 5, 5, 6]
        uf.rank = [3, 0, 1, 0, 2, 1, 1, 0, 0, 0, 0]

        # find I
        uf.find(8)
        #                          0  1  2  3  4  5  6  7  8  9  10
        #                          A  B  C  D  E  F  G  H  I  J  K
        self.assertEqual(uf.pi,   [0, 0, 0, 2, 0, 0, 4, 4, 0, 5, 6])
        self.assertEqual(uf.rank, [3, 0, 1, 0, 2, 1, 1, 0, 0, 0, 0])

        # find K
        uf.find(10)
        #                          0  1  2  3  4  5  6  7  8  9  10
        #                          A  B  C  D  E  F  G  H  I  J  K
        self.assertEqual(uf.pi,   [0, 0, 0, 2, 0, 0, 0, 4, 0, 5, 0])
        self.assertEqual(uf.rank, [3, 0, 1, 0, 2, 1, 1, 0, 0, 0, 0])
        self.verifyConnected(uf)


    def test_unions(self):
        """
        Test from DPV Figure 5.6 by Foster Gorman.
        This test allows for multiple conventions if the subtrees have equal rank:
          1. Point the left subtree to the root of the right subtree (DPV convention)
          2. Point the right subtree to the root of the left subtree
        """
        # Create A, ..., G
        uf = mst.unionFind(7)

        # union(A,D), union(B,E), union(C,F)
        uf.union(0, 3)
        uf.union(1, 4)
        uf.union(2, 5)
        self.assertIn(uf.pi, [[3, 4, 5, 3, 4, 5, 6], [0, 1, 2, 0, 1, 2, 6]])
        self.assertIn(uf.rank, [[0, 0, 0, 1, 1, 1, 0], [1, 1, 1, 0, 0, 0, 0]])

        # union(C,G), union(E,A)
        uf.union(2, 6)
        uf.union(4, 0)
        self.assertIn(uf.pi, [[3, 4, 5, 3, 3, 5, 5], [1, 1, 2, 0, 1, 2, 2]])
        self.assertIn(uf.rank, [[0, 0, 0, 2, 1, 1, 0], [1, 2, 1, 0, 0, 0, 0]])
        for u, v in permutations([0, 1, 3, 4], 2):
            self.assertTrue(uf.areConnected(u, v))
        for u, v in permutations([2, 5, 6], 2):
            self.assertTrue(uf.areConnected(u, v))

        # union(B,G)
        uf.union(1, 6)
        self.assertIn(uf.pi, [[3, 3, 5, 3, 3, 3, 5], [1, 1, 1, 1, 1, 2, 2]])
        self.assertIn(uf.rank, [[0, 0, 0, 2, 1, 1, 0], [1, 2, 1, 0, 0, 0, 0]])

        self.verifyConnected(uf)


if __name__ == '__main__':
    unittest.main()
