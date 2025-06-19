import os

from binary_build_tools.main import main

if __name__ == "__main__":
    main(os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated"))
