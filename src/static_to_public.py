import os
import shutil

def recursive_copy(src,dst):
    #Make sure destination exists, and is a complete mirror of source folder
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    src_content = os.listdir(src)

    for item in src_content:
        source_path = os.path.join(src, item)
        destination_path = os.path.join(dst, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path,destination_path)
        else:
            recursive_copy(source_path,destination_path) 
        print(f"Copying {src} -> {dst}")   

    
