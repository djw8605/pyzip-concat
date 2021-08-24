#!/usr/bin/env python3
import argparse
import os.path
import zipfile


def main():
    parser = argparse.ArgumentParser(description='Contact similarly named files in zip files')
    parser.add_argument("input", nargs="+", help="Input zip files")
    parser.add_argument("output", help="Output zip file")
    args = parser.parse_args()
    input_zips = []

    # A set allows the file name to only be in the list once
    filenames = set()

    # Open each of the input zip files
    for input_zip_name in parser.input:
        zip_file = zipfile.ZipFile(input_zip_name, mode='r')
        input_zips.append(zip_file)
        # Create a list of all of the files in all of the input zips
        filenames.update(zip_file.namelist())

    # Open the output zip file
    output_zip = zipfile.ZipFile(args.output, 'w')

    # For the first zip file, loop through the file names looking for other files
    # May need to sort the namelist
    for zipped_file in filenames:
        # Open the output file
        output_file = output_zip.open(os.path.basename(zipped_file), mode='w')
        # For each zip file in the inputs, add the contents to the same named output file
        for zip_file in input_zips:
            if zipped_file not in zip_file.namelist():
                print("The file {} is not in the zip file {}".format(zipped_file, zip_file.filename))
                continue
            output_file.write(zip_file.read(zipped_file))

        output_file.close()

    # Close everything
    output_zip.close()
    for input_zip in input_zips:
        input_zip.close()



if __name__ == '__main__':
    main()

