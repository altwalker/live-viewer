import random
import string
import time


def generate_random_message(length=30):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class ModelName:

    def edge_A(self):
        print(generate_random_message())
        time.sleep(3)

    def edge_B(self):
        print(generate_random_message())
        time.sleep(3)

    def edge_C(self):
        print(generate_random_message())
        time.sleep(3)

    def edge_D(self):
        print(generate_random_message())
        time.sleep(3)

    def edge_E(self):
        print(generate_random_message())
        time.sleep(3)

    def edge_F(self):
        print(generate_random_message())
        time.sleep(3)

    def edge_G(self):
        print(generate_random_message())
        time.sleep(3)

    def edge_H(self):
        print(generate_random_message())
        time.sleep(3)

    def vertex_A(self):
        print(generate_random_message())
        time.sleep(3)

    def vertex_B(self):
        print(generate_random_message())
        time.sleep(3)

    def vertex_C(self):
        print(generate_random_message())
        time.sleep(3)

    def vertex_D(self):
        print(generate_random_message())
        time.sleep(3)

        if random.randint(0, 10) > 8:
            raise Exception(generate_random_message())

    def vertex_E(self):
        print(generate_random_message())
        time.sleep(3)

    def vertex_F(self):
        print(generate_random_message())
        time.sleep(3)

    def vertex_G(self):
        print(generate_random_message())
        time.sleep(3)
