import random
import unittest
from lru import LRU

SIZES = [1, 2, 10, 1000]

class TestLRU(unittest.TestCase):

    def setUp(self):
        pass

    def _check_kvi(self, valid_keys, l):
        valid_vals = map(str, valid_keys)
        self.assertEquals(valid_keys, l.keys())
        self.assertEquals(valid_vals, l.values())
        self.assertEquals(zip(valid_keys, valid_vals), l.items())

    def test_invalid_size(self):
        self.assertRaises(ValueError, LRU, -1)
        self.assertRaises(ValueError, LRU, 0)

    def test_empty(self):
        l = LRU(1)
        self.assertEquals([], l.keys())
        self.assertEquals([], l.values())

    def test_add_within_size(self):
        for size in SIZES:
            l = LRU(size)
            for i in xrange(size):
                l[i] = str(i)
            self._check_kvi(range(size-1,-1,-1), l)

    def test_delete_multiple_within_size(self):
        for size in SIZES:
            l = LRU(size)
            for i in xrange(size):
                l[i] = str(i)
            for i in xrange(0,size,2):
                del l[i]
            self._check_kvi(range(size-1,0,-2), l)
            for i in range(0,size,2):
                with self.assertRaises(KeyError):
                    l[i]

    def test_delete_multiple(self):
        for size in SIZES:
            l = LRU(size)
            n = size*2
            for i in xrange(n):
                l[i] = str(i)
            for i in xrange(size,n,2):
                del l[i]
            self._check_kvi(range(n-1,size,-2), l)
            for i in xrange(0,size):
                with self.assertRaises(KeyError):
                    l[i]
            for i in xrange(size,n,2):
                with self.assertRaises(KeyError):
                    l[i]

    def test_add_multiple(self):
        for size in SIZES:
            l = LRU(size)
            for i in xrange(size):
                l[i] = str(i)
            l[size] = str(size)
            self._check_kvi(range(size,0,-1), l)

    def test_access_within_size(self):
        for size in SIZES:
            l = LRU(size)
            for i in xrange(size):
                l[i] = str(i)
            for i in xrange(size):
                self.assertEquals(l[i], str(i))
                self.assertEquals(l.get(i,None), str(i))

    def test_access(self):
        for size in SIZES:
            l = LRU(size)
            n = size * 2
            for i in xrange(n):
                l[i] = str(i)
            self._check_kvi(range(n-1,size-1,-1), l)
            for i in xrange(size, n):
                self.assertEquals(l[i], str(i))
                self.assertEquals(l.get(i,None), str(i))

    def test_has_key(self):
        for size in SIZES:
            l = LRU(size)
            for i in xrange(2*size):
                l[i] = str(i)
                self.assertTrue(l.has_key(i))
            for i in xrange(size, 2*size):
                self.assertTrue(l.has_key(i))
            for i in xrange(size):
                self.assertFalse(l.has_key(i))

    def test_capacity_get(self):
        for size in SIZES:
            l = LRU(size)
            self.assertTrue(size == l.get_size())

    def test_capacity_set(self):
        for size in SIZES:
            l = LRU(size)
            for i in range(size+5):
                l[i] = str(i)
            l.set_size(size+10)
            self.assertTrue(size+10 == l.get_size())
            self.assertTrue(len(l) == size)
            for i in range(size+20):
                l[i] = str(i)
            self.assertTrue(len(l) == size+10)
            l.set_size(size+10-1)
            self.assertTrue(len(l) == size+10-1)

    def test_clear(self):
        for size in SIZES:
            l = LRU(size)
            for i in range(size+5):
                l[i] = str(i)
            l.clear()
            for i in range(size):
                l[i] = str(i)
            for i in xrange(size):
                _ = l[random.randint(0,size-1)]
            l.clear()
            self.assertTrue(len(l) == 0)

    def test_hits(self):
        for size in SIZES:
            l = LRU(size)
            for i in range(size):
                l[i] = str(i)

            val = l[0]
            self.assertTrue(l.get_hits() == 1)
            self.assertTrue(l.get_misses() == 0)

            val = l.get(0, None)
            self.assertTrue(l.get_hits() == 2)
            self.assertTrue(l.get_misses() == 0)

            val = l.get(-1, None)
            self.assertTrue(l.get_hits() == 2)
            self.assertTrue(l.get_misses() == 1)

            try:
                val = l[-1]
            except:
                pass

            self.assertTrue(l.get_hits() == 2)
            self.assertTrue(l.get_misses() == 2)

            l.clear()
            self.assertTrue(len(l) == 0)
            self.assertTrue(l.get_hits() == 0)
            self.assertTrue(l.get_misses() == 0)

if __name__ == '__main__':
    unittest.main()
