import os
import shutil


def transfer(from_dir, to_dir):
    shutil.rmtree(to_dir)
    os.mkdir(to_dir)
    if os.path.exists(from_dir) and os.path.exists(to_dir):
        for item in os.listdir(from_dir):
            if os.path.isfile(os.path.join(from_dir, item)):
                shutil.copy(os.path.join(from_dir, item), to_dir)
            else:
                new_dir = os.path.join(to_dir, item)
                os.mkdir(new_dir)
                transfer(os.path.join(from_dir, item), new_dir)
    return
        