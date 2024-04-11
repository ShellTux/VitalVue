BUILD_DIR = build

ARCHIVE             = BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip
INSTALLATION_MANUAL = installation-manual.pdf
PANDOC_OPTS         = --variable=theme:Warsaw --highlight-style=assets/onehalfdark.theme
PRESENTATION        = presentation.pdf
REPORT              = relatorio.pdf
USER_MANUAL         = user-manual.pdf

VENV        = venv
PYTHON     := ./$(VENV)/bin/python3
PIP        := ./$(VENV)/bin/pip
PRE_COMMIT := ./$(VENV)/bin/pre-commit

all: venv $(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL) $(PRESENTATION)

$(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL): %.pdf: $(BUILD_DIR)/docs/%.md
	pandoc --output=$@ $<

$(PRESENTATION): %.pdf: $(BUILD_DIR)/docs/%.md
	pandoc $(PANDOC_OPTS) --output=$@ --to=beamer $<

$(BUILD_DIR)/%.md: %.md
	mkdir --parents $(shell dirname $@)
	cp $< $@
	sed -i 's|/assets|assets|g' $@

.PHONY: archive
archive: $(ARCHIVE)

$(ARCHIVE): $(REPORT) $(PRESENTATION) $(USER_MANUAL) $(INSTALLATION_MANUAL)
	git archive --output=$@ $(^:%=--add-file=%) HEAD

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --requirement requirements.txt

.PHONY: venv
venv: $(VENV)/bin/activate

pre-commit: venv
	$(PRE_COMMIT) install

clean:
	rm -rf $(VENV) $(BUILD_DIR) $(REPORT) $(ARCHIVE)
	find . -type f -name '*.pyc' -delete

run: $(VENV)
	(sleep 1 && xdg-open "http://127.0.0.1:8080") &
	$(PYTHON) ./src/app.py
