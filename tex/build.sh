#!/bin/sh
docker run --rm -i --user="$(id -u):$(id -g)" --net=none -v "$PWD":/data blang/latex bash -c "pdflatex dyplom-utf8-unix.tex; pdflatex praca.tex;";
# pdflatex dyplom-utf8-unix.tex
# pdflatex praca.tex
rm dyplom-utf8-unix.aux;
rm dyplom-utf8-unix.log;
rm dyplom-utf8-unix.toc;
rm praca.aux;
rm praca.log;
rm praca.toc;
