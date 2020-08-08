from kivy.logger import Logger

import os

Logger.info("FaceHandler: Importing 'face_recognition'. . .")
import face_recognition  # noqa: E402

# import threading


# def threaded_import():
#     import importlib
#     global face_recognition
#     face_recognition = importlib.import_module('face_recognition')


# face_recognition = None
# thread = threading.Thread(target=threaded_import)
# thread.daemon = True
# thread.start()


class FaceHandler:
    faces_dir = 'data/local/cropped'
    filenames = []
    local_encodings = []
    tolerance = 0.4

    def __init__(self):
        self.initialize_local_encodings()

    def initialize_local_encodings(self):
        blacklist = ('.gitignore')
        for image in os.listdir(self.faces_dir):
            if image in blacklist:
                continue

            path = f'{self.faces_dir}/{image}'

            self.filenames.append(path)

            Logger.info(f"FaceHandler: Loading '{path}'. . .")
            loaded = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(loaded)[0]
            self.local_encodings.append(encoding)

    def find_match(self, image):
        current = face_recognition.load_image_file(image)
        encoding = face_recognition.face_encodings(current)[0]

        # for tol in [i/10 for i in range(1, 6 + 1)]:
        #     result = face_recognition.compare_faces(
        #         self.local_encodings, encoding, tolerance=tol)
        #     print(result)
        #     print()

        result = face_recognition.compare_faces(
            self.local_encodings, encoding, tolerance=self.tolerance,
        )
        print(result)


if __name__ == '__main__':
    instance = FaceHandler()

    for file in os.listdir('data/received/test_images'):
        print(file)
        instance.find_match(f'data/received/test_images/{file}')
        print()
