
def validImageFile(file_path):
    """
    Check if the file is a valid image file.
    """
    valid_extensions = [".jpg", ".jpeg", ".png"]
    return any(file_path.lower().endswith(ext) for ext in valid_extensions)