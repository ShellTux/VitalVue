BUILD_DIR = build

relatorio.pdf: $(BUILD_DIR)/docs/report.md
	pandoc --output=$@ $<

$(BUILD_DIR)/%.md: %.md
	mkdir --parents $(shell dirname $@)
	cp $< $@
	sed -i 's|/assets|assets|g' $@

.PHONY: archive
archive: BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip

BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip: relatorio.pdf
	git archive --output=$@ --add-file=$< HEAD

clean:
	rm -rf $(BUILD_DIR) relatorio.pdf
