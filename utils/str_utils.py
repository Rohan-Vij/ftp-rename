"""String processing utilities."""
import os


def parse_file_name(file_name, patterns):
    """
    Parse a file name to extract the item id, image type, and item name.

    :param file_name: the file name to parse
    :param patterns: a list of patterns to match

    :returns: a tuple of the item id, image type, and item name
    """

    file_name, file_extension = os.path.splitext(file_name)

    split_name = file_name.split("-")

    item_id = split_name[0]
    item_name = ""
    item_image_type = ""

    # Only define the item name as the middle value of split_name if its length if more than 2
    # If length is 3 = [x, name, x]
    # If length is less than 2 = [x, name]
    # try:
    #     item_name = "-".join(split_name[1:-1]
    #                          ) if len(split_name) > 2 else split_name[1]
    # except IndexError as error:
    #     raise IndexError from error

    endings = list(filter(file_name.endswith, patterns))

    # If the last three characters are _th
    if file_name[-3:] == "_th":
        print("th")
        item_image_type = file_name[-3:]  # The image type is _th
        print(item_image_type + "\n")
        # The name does not include the last 3 characters
        item_name = "-".join(split_name[1:])[:-3]
    elif len(endings) > 0:
        # The image type is the longest ending
        item_image_type = max(endings, key=len)
        item_name = "-".join(split_name[1:]).replace(max(endings, key=len), '')
    else:
        item_image_type = ""
        item_name = "-".join(split_name[1:])

    return item_id, item_image_type, file_extension, item_name


def rewrite_file_name(item_id, item_image_type, file_extension, original_item_name, new_item_name):

    """
    Rewrite a file name with the given item id, image type, file extension, and item name.

    :param item_id: the item id
    :param item_image_type: the item image type
    :param file_extension: the file extension
    :param original_item_name: additional argument to override the item name and type
    :param new_item_name: the item name

    :returns: the rewritten file name, whether the item was renamed
    """

    new_item_name = new_item_name.replace(" ", "-").lower()
    original_item_name = original_item_name.replace(" ", "-").lower()

    if item_image_type:
        return f"{item_id}-{new_item_name}{item_image_type}{file_extension}", True
    return f"{item_id}-{original_item_name}{file_extension}", False
