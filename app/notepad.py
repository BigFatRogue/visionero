if __name__ == '__main__':
    # Для запуска через IDE

    import sys
    from pathlib import Path
    test_path = str(Path(__file__).parent.parent)
    sys.path.append(test_path)


from scripts.source_generator import generator_message
from app.schemes.scheme_data import SourceDataSheme

