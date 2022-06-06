"""Testing file."""
from utils.str_utils import parse_file_name, rewrite_file_name
from utils.load_configs import load_file

config = load_file("config.yaml")

CATEGORIES = config["CATEGORIES"]
IMAGE_PATTERNS = config["PATTERNS"]["IMAGES"]

file_names = ["7123-some-example-txt-detail-high.jpg", "7123-some-example-txt-detail.jpg", "7123-some-example-txt-detail-low.jpg"]

for file_name in file_names:
    print(file_name)
    parsed = parse_file_name(file_name, IMAGE_PATTERNS)
    print(*parsed[:-1])
    rewritten = rewrite_file_name(*parsed, "more example text")[0]

    print(parsed)
    print(rewritten)
    print("\n")
