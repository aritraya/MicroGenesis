import sys
from src.core.main import main

if __name__ == "__main__":
    sys.argv = ["main", "--config-file", "./tests/resource/quick_test_config.json"]
    main()