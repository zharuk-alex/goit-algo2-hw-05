import mmh3


class BloomFilter:
    def __init__(self, size, num_hashes):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Size must be a positive integer.")
        if not isinstance(num_hashes, int) or num_hashes <= 0:
            raise ValueError("Number of hashes must be a positive integer.")

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        if not isinstance(item, str) or not item:
            raise ValueError("Item must be a non-empty string.")

        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        if not isinstance(item, str) or not item:
            return False

        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True
