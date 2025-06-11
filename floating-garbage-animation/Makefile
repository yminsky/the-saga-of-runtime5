.PHONY: all clean

all: index.html

index.html:
	dune build index.html
	cp _build/default/index.html .

clean:
	dune clean
	rm -f index.html