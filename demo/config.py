from pathlib import Path
import base64


def img2bytes(path):
    img_bytes = Path(path).read_bytes()
    return base64.b64encode(img_bytes).decode()


MODEL_TIFUKNN = "TIFU KNN"
MODEL_POPULAR = "Popularity-based"

ITEM_IMG_WIDTH = 175

ITEMS_AMOUNT = 60
ITEMS_PER_ROW = 5

DEFAULT_ITEMS_AMOUNT = 3

ITEMS_MAPPING = "../data/item_mapping.json"
RECOM_BASE_TIFU_FULL = '../data/recom_base_tifu_full.csv'
ITEMS_MAPPING_TIFU = "../data/item_mapping_tifu.json"

REPO_LINK = "https://github.com/sokolcom/mts-teta-nbr"

HTML_CREDITS = \
    """[<img src='data:image/png;base64,{0}' class='img-fluid' width=25 height=25>]({1}) <small> Demo stand | Team 42 </small>""" \
    .format(img2bytes("../images/github_logo.png"), REPO_LINK)


# Stubs
DATA_PATH = "../data/apriori_top_20.csv"
RAND_IMAGE = "https://picsum.photos/200/300"
DESCRIPTION = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
STUB_METRICS = { "current_f1": 0.897, "prev_f1": 0.826 }