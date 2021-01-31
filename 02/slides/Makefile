.SILENT: diagrams-all

diagrams-all:
	find diagrams -name "diagram-*" -exec python {} \;
	mv *.png images/

render-slides: diagrams-all
	asciidoctor-web-pdf ./02.adoc --template-require ../../slides-template/template.js

