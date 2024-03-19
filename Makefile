relatorio.pdf: docs/report.md
	pandoc --output=$@ --resource-path=assets $<

.PHONY: archive
archive: BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip

BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip: relatorio.pdf
	git archive --output=$@ --add-file=$< HEAD
