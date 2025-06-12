.PHONY: all clean heap-animation floating-garbage-animation format

all: heap-animation floating-garbage-animation

heap-animation: heap-marking-diagram/heap_animation.html

floating-garbage-animation: floating-garbage-animation/index.html

heap-marking-diagram/heap_animation.html:
	dune build heap-marking-diagram/generate_heap_animation.exe
	dune exec heap-marking-diagram/generate_heap_animation.exe

floating-garbage-animation/index.html:
	dune build floating-garbage-animation/generate_animation.exe
	dune exec floating-garbage-animation/generate_animation.exe

clean:
	dune clean
	rm -f heap-marking-diagram/heap_animation.html
	rm -f floating-garbage-animation/index.html

format:
	dune build @fmt --auto-promote