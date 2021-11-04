import os
import sys
import argparse

from make_mocs import filter_directories, moc_file_path_for_directory, index_content_for_directory, update_existing_moc


def process_all_directories(directory, args):
    for root, dirs, files in os.walk(directory):
        filter_directories(dirs)
        dirs.sort()
        process_directory(root, dirs, files)


def process_directory(root, dirs, files):
    moc_file_path = moc_file_path_for_directory(root)
    new_index_with_delimiters = index_content_for_directory(root, dirs, files)
    if os.path.exists(moc_file_path):
        rewrite_existing_moc_file(moc_file_path, new_index_with_delimiters)
    else:
        write_new_moc_file(moc_file_path, new_index_with_delimiters)


def rewrite_existing_moc_file(moc_file_path, new_index_with_delimiters):
    with open(moc_file_path, 'r') as input:
        initial_content = input.readlines()
    with open(moc_file_path, 'w') as output:
        output.write(update_existing_moc(initial_content, new_index_with_delimiters))


def write_new_moc_file(moc_file_path, new_index_with_delimiters):
    # TODO Create this from a file template
    with open(moc_file_path, 'w') as output:
        output.write(new_index_with_delimiters)


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Create and update MOCs, mimicking Zoottelkeeper output"
    )
    # parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args = parser.parse_args(argv)

    process_all_directories('../..', args)


if __name__ == "__main__":
    main()
