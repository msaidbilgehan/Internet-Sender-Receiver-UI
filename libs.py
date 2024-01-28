import sys

library_path = "/".join(sys.path[0].replace("\\", "/").split("/")[:-1])
sys.path.append(library_path)

working_dir = "/".join(__file__.replace("\\", "/").split("/")[:-1]) + "/"

import global_libs
