all: heap_marking.svg heap_marking.png

heap_marking.svg: generate_heap_diagram.py
	python3 generate_heap_diagram.py

heap_marking.png: heap_marking.svg
	convert heap_marking.svg heap_marking.png

clean:
	rm -f heap_marking.svg heap_marking.png

.PHONY: all clean