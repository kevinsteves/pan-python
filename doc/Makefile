RST2HTML = rst2html
OPTIONS =
SOURCE = panxapi.html pan.xapi.html

.SUFFIXES: .rst .html
.rst.html:
	$(RST2HTML) $(OPTIONS) $< $@

all: $(SOURCE)

clean:
	rm -f $(SOURCE)
