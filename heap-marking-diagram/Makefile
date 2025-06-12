all: heap_marking.svg heap_marking.png heap_animation.html

heap_marking.svg: generate_heap_diagram.py
	python3 generate_heap_diagram.py

heap_marking.png: heap_marking.svg
	convert heap_marking.svg heap_marking.png

heap_animation.html: generate_heap_animation.py
	python3 generate_heap_animation.py

clean:
	rm -f heap_marking.svg heap_marking.png heap_animation.html

.PHONY: all clean