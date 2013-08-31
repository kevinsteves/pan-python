# $Id: Makefile,v 1.1 2013/03/06 01:51:17 stevesk Exp $

RST2HTML = rst2html
OPTIONS =
SOURCE = panxapi.html pan.xapi.html

.SUFFIXES: .rst .html
.rst.html:
	$(RST2HTML) $(OPTIONS) $< $@

all: $(SOURCE)

clean:
	rm -f $(SOURCE)
