from sys import argv
from scss import Compiler

def compile_scss_file(filename: str) -> None:
    assert '.scss' in filename, filename

    with open(filename.replace('.scss', ''), 'wb') as fh:
        fh.write(
            Compiler().compile_string(open('static/style.css.scss', 'rb').read()),
        )

if __name__ == '__main__':
    compile_scss_file(argv[1])
