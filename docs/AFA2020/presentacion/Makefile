
NAME=presentacion_RAFA2020

BUILDTEXT=pdflatex $(NAME).tex
# BUILDBIB=bibtex $(NAME).aux

.SUFFIXES:
.SUFFIXES: .pdf .tex
.PHONY: clean buildclean view

$(NAME).pdf: src/$(NAME).tex src/src_figs/* src/*
	mkdir -p build
	cp ./src/$(NAME).tex ./build/
	cp -r ./src/src_figs ./build/
	# Compile Latex and Bibliography
	cd build; $(BUILDTEXT);	\
						$(BUILDTEXT); \
						$(BUILDTEXT); \
						cp $(NAME).pdf ..

clean: buildclean
	rm -f $(NAME).pdf 

buildclean:
	rm -fr build

view: $(NAME).pdf 
	evince $(NAME).pdf &

