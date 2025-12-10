import os

def clean_directory(root_path):
    if not os.path.isdir(root_path):
        print(f"the root path mentioned{root_path} is not availabe")
        return
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath,filename)
            try:
                file_size = os.path.getsize(file_path)
                if file_size > 100 * 1024 * 1024:
                    os.remove(file_path)
            except OSError  as e:
                print(f"error processingfile {e}")


    for dirpath, dirnames, filenames in os.walk(root_path, topdown = False):
        try:
            if not os.listdir(dirpath):
                print(f"Deleting empty directory: {dirpath}")
                os.rmdir(dirpath)

        except Exception as e:
            print(f"error processing directory {dirpath} : {e}")










