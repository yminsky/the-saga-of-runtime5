all: heap_animation.html

generate_heap_animation.exe: generate_heap_animation.ml dune-project dune
	dune build generate_heap_animation.exe

heap_animation.html: generate_heap_animation.exe
	dune exec ./generate_heap_animation.exe

clean:
	rm -f heap_animation.html
	dune clean

.PHONY: all clean