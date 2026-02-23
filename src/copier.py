import os
import shutil

def copier(source, destination, first_call=True):
    if os.path.exists(destination) and first_call:
        shutil.rmtree(destination)
    os.mkdir(destination)
    if os.path.exists(source):
        for item in os.listdir(source):
            src_path = os.path.join(source, item)
            dst_path = os.path.join(destination, item)

            if os.path.isdir(src_path):
                print(f"Recursive call to copier for path: {src_path}")
                copier(src_path, dst_path, False)
            else:
                shutil.copy(src_path, dst_path)
                print(f"Copied {src_path} to {dst_path}")
    