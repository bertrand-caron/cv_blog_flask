from os.path import exists, basename, dirname, join
from glob import glob
from yaml import load, dump

DATA_DIR = join(dirname(dirname(__file__)), 'data')

CONFIG_DIR = join(dirname(dirname(__file__)), 'config')

def example_yml_file(yml_file):
    return yml_file + '.example'

def recursive_assert_object_match(object_1, object_2, debug=False):
    if debug:
        print
        print 'OBJECTS: {0}(type={1}) {2}(type={3})'.format(object_1, type(object_1), object_2, type(object_2))

    if type(object_1) == type(object_2):
        if type(object_1) == type(object_2) == dict:

            def check_same_keys():
                if debug:
                    if set(object_1.keys()) != set(object_2.keys()):
                        print 'ERROR: MISSING KEYS {0}'.format(set(object_1.keys()) ^ set(object_2.keys()))

                return set(object_1.keys()) == set(object_2.keys())

            def check_same_value_for_key(key):
                if debug:
                    if not recursive_assert_object_match(object_1[key], object_2[key]):
                        print 'ERROR: DIFFERENT VALUE FOR KEY {0}'.format(key)
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
        if debug:
            print 'OBJECT MISMATCH: {0} != {1}'.format(type(object_1), type(object_2))

        return False

def recursive_obfuscation(an_object):
    if type(an_object) == list:
        return map(
            recursive_obfuscation,
            an_object,
        )
    elif type(an_object) == dict:
        return dict(
            [
                (key, recursive_obfuscation(value))
                for (key, value)
                in an_object.items()
            ],
        )
    elif type(an_object) in (str, unicode, int, float):
        if type(an_object) in (str, unicode):
            return 'Loreum Ipsum'
        elif type(an_object) == int:
            return 0
        elif type(an_object) == float:
            return 0.0
        else:
            raise Exception('Unknown type: {0}'.format(type(an_object)))
    else:
        raise Exception('Unknown type: {0}'.format(type(an_object)))

def check_example_yml_files():
    for yml_file in glob(join(DATA_DIR, '*.yml')) + glob(join(DATA_DIR, 'posts', '*.yml')) + [join(CONFIG_DIR, 'config.yml')]:

        yml_content = load(open(yml_file).read())

        example_yml_content = recursive_obfuscation(yml_content)

        assert recursive_assert_object_match(yml_content, example_yml_content)

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
    assert recursive_assert_object_match({'a': 1}, {'a': 'bob'}) == False
    assert recursive_assert_object_match({'a': 1}, {'b': 'bob'}) == False
    assert recursive_assert_object_match(['a'], [1]) == False

    check_example_yml_files()
