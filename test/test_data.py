from os.path import exists, dirname, join
from glob import glob
from typing import Any
from yaml import load, dump

DATA_DIR = join(dirname(dirname(__file__)), 'data')

CONFIG_DIR = join(dirname(dirname(__file__)), 'config')

def example_yml_file(yml_file: str) -> str:
    return yml_file + '.example'

DEBUG = False

def recursive_assert_object_match(object_1: Any, object_2: Any, debug: bool = DEBUG) -> Any:
    if debug:
        print()
        print('OBJECTS:\n- {0} (type={1})\n- {2} (type={3})'.format(object_1, type(object_1), object_2, type(object_2)))

    if type(object_1) == type(object_2):
        if type(object_1) == type(object_2) == dict:
            def check_same_keys() -> bool:
                if debug:
                    if set(object_1.keys()) != set(object_2.keys()):
                        print('ERROR: MISSING KEYS {0}'.format(set(object_1.keys()) ^ set(object_2.keys())))

                return set(object_1.keys()) == set(object_2.keys())

            def check_same_value_for_key(key: Any):
                if debug:
                    if not recursive_assert_object_match(object_1[key], object_2[key]):
                        print('ERROR: DIFFERENT VALUE FOR KEY {0}'.format(key))
                return recursive_assert_object_match(object_1[key], object_2[key])

            return (
                check_same_keys()
                and
                all(
                    [
                        check_same_value_for_key(key)
                        for key in
                        set(object_1.keys()) & set(object_2.keys())
                    ]
                )
            )
        elif type(object_1) == type(object_2) == list:
            return recursive_assert_object_match(object_1[0], object_2[0])
        else:
            return True
    else:
        raise Exception('OBJECT MISMATCH: {0} (object={2}) != {1} (object={3})'.format(type(object_1), type(object_2), object_1, object_2))

DO_NOT_OBFUSCATE_KEYS = [
    'icon',
    'rating',
]

LOREUM_IPSUM = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua' * 10).split()

def recursive_obfuscation(an_object: Any) -> Any:
    def raise_unknown_type():
        raise Exception(
            'Unknown type: {0}(type={1})'.format(
                an_object,
                type(an_object),
            ),
        )

    if type(an_object) == list:
        return list(map(
            recursive_obfuscation,
            [an_object[0]], # Keep only the first object of each list, for the sake of concision
        ))
    elif type(an_object) == dict:
        return {
            (
                key,
                value if key in DO_NOT_OBFUSCATE_KEYS else recursive_obfuscation(value),
            )
            for (key, value) in an_object.items()
        }
    elif type(an_object) in (str, int, float):
        if type(an_object) == str:
            return ' '.join([loreum_ipsum_word for (word, loreum_ipsum_word) in zip(an_object.split(), LOREUM_IPSUM)])
        elif type(an_object) == int:
            return 0
        elif type(an_object) == float:
            return 0.0
        else:
            raise_unknown_type()
    elif type(an_object) == bool:
        return an_object
    elif type(an_object) == type(None):
        return an_object
    else:
        raise_unknown_type()

def check_example_yml_files():
    for yml_file in glob(join(DATA_DIR, '*.yml')) + glob(join(DATA_DIR, 'posts', '*.yml')) + [join(CONFIG_DIR, 'config.yml')]:

        yml_content = load(open(yml_file).read())

        try:
            example_yml_content = recursive_obfuscation(yml_content)
        except Exception as e:
            raise Exception('ERROR in {0}: {1}'.format(yml_file, e))

        assert recursive_assert_object_match(yml_content, example_yml_content, debug=True)

        with open(example_yml_file(yml_file), 'w') as fh:
            fh.write(
                dump(
                    example_yml_content,
                    indent=True,
                    default_flow_style=False,
                ),
            )

        assert exists(example_yml_file(yml_file)), 'ERROR: yml_file {0} does not have an example (missing file "{1}")'.format(
            yml_file,
            example_yml_file(yml_file),
        )


if __name__ == '__main__':
    #assert recursive_assert_object_match({'a': 1}, {'a': 'bob'}) == False
    #assert recursive_assert_object_match({'a': 1}, {'b': 'bob'}) == False
    #assert recursive_assert_object_match(['a'], [1]) == False

    check_example_yml_files()
