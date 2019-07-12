target=report

all:
	pdflatex $(target).tex
	pdflatex $(target).tex
	make clean

clean:
	rm -f *.aux *.log *.out *.dvi
	cd secs && rm -f *.aux *.log
