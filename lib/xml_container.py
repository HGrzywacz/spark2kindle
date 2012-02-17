def make_file(index, sections):
	"""Class containing HTML (xml?) code necessary for creating table of content
    file toc.html.

    Args:
	index: Index class object, it's attribute dirname is used here.
	sections: list of Section class objects.
    """

    print("Generating table of contents.")

    f = file(index.dirname + 'toc.html','w')

	f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' + "\n")
	f.write('<html xmlns="http://www.w3.org/1999/xhtml">' + "\n")
	f.write("\n" + '<head><title>Table of Contents</title></head>' + "\n")
	f.write("\n" + "\n" + '<body>' + "\n" + '<div>' + "\n" + ' <h1><b>TABLE OF CONTENTS</b></h1>' + "\n" + '<br />')

	# lista:
	f.write('<div><ul>' + "\n")
	for section in sections:
		f.write('<li><a href="' + section.filename + '">' + section.title + '</a></li>' + "\n")
	f.write('</ul></div><br />' + "\n")
	f.close()



class Opf(object):
	"""Class containing XML code necessary for creating opf file.

    Has no attributes. Probably should be static. [TODO]
    Opf file contains metadata, manifest and spine.
    Also tours and guide - those aren't used though.

    Args:
	index: Index class object, it's attribute dirname is used here.
	sections: list of Section class objects.
    """

    @staticmethod
    def make_file(index, sections):
	    f = file(index.dirname + "book.opf",'w')

	f.write('<?xml version="1.0" encoding="utf-8"?>' + "\n")
	f.write('<package unique-identifier="uid">' + "\n")
	f.write("\t" + '<metadata>' + "\n")
	f.write("\t\t" + '<dc-metadata xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">' + "\n")
	f.write("\t\t" + '<dc:Title>Sparknotes: ' + index.title + '</dc:Title>' + "\n")
	f.write("\t\t" + '<dc:Creator>Sparknotes</dc:Creator>' + "\n")
	f.write("\t\t" + '<dc:Language>en-us</dc:Language>' + "\n")
	f.write("\t\t" + '<dc:Identifier id="uid">9095C522E6</dc:Identifier>' + "\n")
	f.write("\t" +  '</dc-metadata>' + "\n" + "\n")

	f.write("\t" + '<x-metadata>' + "\n")
	f.write("\t\t" + '<output encoding="utf-8"></output>' + "\n")
	f.write("\t\t" + '<EmbeddedCover>cover.jpg</EmbeddedCover>' + "\n")
	f.write("\t" + '</x-metadata>' + "\n" + '</metadata>' + "\n" + "\n")
	# manifest
	f.write('<manifest>' + "\n")
	f.write('<item id="item1" media-type="application/xhtml+xml" href="toc.html"></item>' + "\n")

	i = 1
	for section in sections:
		i = i + 1
	    f.write('<item id="item' + str(i) + '" media-type="application/xhtml+xml" href="' + section.filename + '"></item>' + "\n")

	f.write('<item id="My_Table_of_Contents" media-type="application/x-dtbncx+xml" href="toc.ncx"/>' + "\n")
	f.write('</manifest>' + "\n")

	f.write('<spine toc="My_Table_of_Contents">' + "\n")
	f.write('<itemref idref="item1"/>' + "\n")
	i = 1
	for section in sections:
		i = i + 1
	    f.write('<itemref idref="item' + str(i) + '"/>' + "\n")

	f.write('</spine><tours></tours><guide></guide></package>' + "\n")

	f.close()


class Ncx(object):
	"""Class containing XML code necessary ncx file.

    NCX file is responsible for little dots seen on the bottom of the Kindle
    screen. At least that's what original author (namely me) was able to
    figure out.

    Args:
	index: Index class object, it's attribute dirname is used here.
	sections: list of Section class objects.
    """


    @staticmethod
    def make_file(index, sections):
	    f = file(index.dirname + "toc.ncx",'w')

	f.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
	f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">' + "\n")
	f.write('<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en-US">' + "\n" +"\n")
	f.write('<head>' + "\n\t")
	f.write('<meta name="dtb:uid" content="BookId"/>' + "\n\t" + '<meta name="dtb:depth" content="2"/>' + "\n\t" + '<meta name="dtb:totalPageCount" content="0"/>')
	f.write("\n\t" + '<meta name="dtb:maxPageNumber" content="0"/>' + "\n" + '</head>' + "\n\t")

	f.write('<docTitle><text>' + index.title + '</text></docTitle>' + "\n")
	f.write('<docAuthor><text>' + index.author + '</text></docAuthor>' + "\n\n" + '<navMap>' + "\n")

	f.write('<navPoint class="toc" id="toc" playOrder="1">' + "\n")
	f.write('<navLabel>' + "\n" + '<text>Table of Contents</text>' + "\n" + '</navLabel>' + "\n")
	f.write('<content src="toc.html"/>' + "\n" + '</navPoint>' + "\n\n")

	i = 1
	for section in sections:
		i = i + 1
	    f.write('<navPoint class="' + section.filename + '" id="' + section.filename + '" playOrder="' + str(i) + "\">\n")
	    f.write('<navLabel>' + "\n" + '<text>' + section.title + '</text>' + "\n" + '</navLabel>' + "\n")
	    f.write('<content src="' + section.filename + '"/>' + "\n" + '</navPoint>' + "\n\n")

	f.write('</navMap>' + "\n" + '</ncx>' + "\n")
	f.close()
