import time
import string
import random


def genreate_random_message(length=30):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class ModelName:

    def edge_A(self):
        print(genreate_random_message())
        time.sleep(3)

    def edge_B(self):
        print(genreate_random_message())
        time.sleep(3)

    def edge_C(self):
        print(genreate_random_message())
        time.sleep(3)

    def edge_D(self):
        print(genreate_random_message())
        time.sleep(3)

    def edge_E(self):
        print(genreate_random_message())
        time.sleep(3)

    def edge_F(self):
        print(genreate_random_message())
        time.sleep(3)

    def edge_G(self):
        print(genreate_random_message())
        time.sleep(3)

    def edge_H(self):
        print(genreate_random_message())
        time.sleep(3)

    def vertex_A(self):
        print(genreate_random_message())
        time.sleep(3)

    def vertex_B(self):
        print(genreate_random_message())
        time.sleep(3)

    def vertex_C(self):
        print(genreate_random_message())
        time.sleep(3)

    def vertex_D(self):
        print(genreate_random_message())
        time.sleep(3)

        if random.randint(0, 10) > 8:
            raise Exception(genreate_random_message())

    def vertex_E(self):
        print(genreate_random_message())
        time.sleep(3)

    def vertex_F(self):
        print(genreate_random_message())
        time.sleep(3)

    def vertex_G(self):
        print(genreate_random_message())
        time.sleep(3)
