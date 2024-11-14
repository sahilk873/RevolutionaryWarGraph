def read_and_split_text(file_path: str) -> list[str]:
    """
    Reads the text file and splits it into sections based on double newlines.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    sections = text.strip().split('\n\n')
    sections = [section.strip() for section in sections if section.strip()]
    return sections