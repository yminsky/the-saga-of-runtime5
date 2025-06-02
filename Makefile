.PHONY: slides clean

# Default target
slides: talk.html

# Convert markdown to reveal.js HTML presentation
talk.html: talk.md
	pandoc -t revealjs -s \
		--from markdown \
		--to revealjs \
		--slide-level=1 \
		--variable revealjs-url=https://unpkg.com/reveal.js@4.6.1 \
		--output talk.html \
		talk.md

# Clean generated files
clean:
	rm -f talk.html

# Show help
help:
	@echo "Available targets:"
	@echo "  slides   - Generate HTML presentation from markdown"
	@echo "  clean    - Remove generated files"
	@echo "  help     - Show this help message"
