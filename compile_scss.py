from sass import compile_string
from sys import argv

def compile_scss_file(filename):
    assert '.scss' in filename

    with open(filename.replace('.scss', ''), 'w') as fh:
        fh.write(
            compile_string(open('static/style.css.scss').read()),
        )

if __name__ == '__main__':
    compile_scss_file(argv[1])
