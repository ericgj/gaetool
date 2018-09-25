import os
import os.path
import shutil

def remove_and_create_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

def copy_files_within(source, dest, force=False):
    for (root, dirs, files) in os.walk(source):
        for item in dirs:
            src_path = os.path.join(root, item)
            dst_path = os.path.join(dest, src_path.replace(source + '/',''))
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)

        for item in files:
            src_path = os.path.join(root, item)
            dst_path = os.path.join(dest, src_path.replace(source + '/',''))
            if os.path.exists(dst_path):
                if force:
                    shutil.copy2(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
        
