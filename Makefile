BUILD_DIR = build

ARCHIVE = BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip
REPORT = relatorio.pdf

$(REPORT): $(BUILD_DIR)/docs/report.md
	pandoc --output=$@ $<

$(BUILD_DIR)/%.md: %.md
	mkdir --parents $(shell dirname $@)
	cp $< $@
	sed -i 's|/assets|assets|g' $@

.PHONY: archive
archive: $(ARCHIVE)

$(ARCHIVE): $(REPORT)
	git archive --output=$@ --add-file=$< HEAD

clean:
	rm -rf $(BUILD_DIR) $(REPORT) $(ARCHIVE)