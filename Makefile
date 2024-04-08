BUILD_DIR = build

ARCHIVE             = BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip
REPORT              = relatorio.pdf
PRESENTATION        = presentation.pdf
USER_MANUAL         = user-manual.pdf
INSTALLATION_MANUAL = installation-manual.pdf
PANDOC_OPTS         = --variable=theme:Warsaw --highlight-style=assets/onehalfdark.theme

%.pdf: $(BUILD_DIR)/%.md
	pandoc $(PANDOC_OPTS) --output=$@ $<

$(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL): %.pdf: $(BUILD_DIR)/docs/%.md
	pandoc --output=$@ --to=beamer $<

$(PRESENTATION): %.pdf: $(BUILD_DIR)/docs/%.md
	pandoc $(PANDOC_OPTS) --output=$@ --to=beamer $<

$(BUILD_DIR)/%.md: %.md
	mkdir --parents $(shell dirname $@)
	cp $< $@
	sed -i 's|date: date|date: '$(shell date +'%d/%m/%Y')'|' $@
	sed -i 's|/assets|assets|g' $@

.PHONY: archive
archive: $(ARCHIVE)

$(ARCHIVE): $(REPORT) $(PRESENTATION) $(USER_MANUAL) $(INSTALLATION_MANUAL)
	git archive --output=$@ $(^:%=--add-file=%) HEAD

clean:
	rm -rf $(BUILD_DIR) $(REPORT) $(ARCHIVE)
