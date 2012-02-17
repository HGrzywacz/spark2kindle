import sys
import os
import shutil
import platform

from lib.spark import SparkIndex, SparkSection
import lib.xml_containers


def main():
    adress = str(sys.argv[1])
    print(adress)
    index = SparkIndex(adress)

    sections = list()

    # Simple for loop appends Section class objects to list. Index.sections
    # is a list of tuples {name, url}. I found this complicated, thus strange
    # name section_name_url_tuple used to prevent confusion.

    for section_name_url_tuple in index.sections:
        section = SparkSection(section_name_url_tuple, index)
        sections.append(section)

    #toc = Toc(index, sections)
    lib.xml_containers.make_toc(index, sections)
    lib.xml_containers.make_ncx(index, sections)
    lib.xml_containers.make_opf(index, sections)

    shutil.copy('lib/styles.css', index.dirname)
    shutil.copy('lib/cover.jpg', index.dirname)

    o_filename = index.dirname_no_slash + ".mobi"

    if platform.system() == 'Linux':
        os.system('./kindlegen ' + index.dirname + 'book.opf' +
                  ' -o ' + o_filename)
    elif (platform.system() == 'Windows') or (platform.system() == 'Microsoft'):
        os.system('start kindlegen ' + index.dirname + 'book.opf')
    else:
        os.system('./kindlegen ' + index.dirname + 'book.opf')


    shutil.move(index.dirname + o_filename, "books/")

if __name__ == "__main__":
    main()

