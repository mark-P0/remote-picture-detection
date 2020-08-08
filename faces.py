import os
# import face_recognition


class FaceHandler:
    faces_dir = 'data/local'

    def __init__(self):
        pass

    def find_match(self):
        pass


if __name__ == '__main__':
    instance = FaceHandler()

    test = os.listdir(instance.faces_dir)
    print(test)
