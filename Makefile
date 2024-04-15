BUILD_DIR = build

ARCHIVE             = BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip
INSTALLATION_MANUAL = installation-manual.pdf
PRESENTATION        = presentation.pdf
REPORT              = relatorio.pdf
USER_MANUAL         = user-manual.pdf
PANDOC_OPTS         = \
		      --variable=theme:Warsaw \
		      --highlight-style=assets/onehalfdark.theme

VENV        = venv
PYTHON     := ./$(VENV)/bin/python3
PIP        := ./$(VENV)/bin/pip
PRE_COMMIT := ./$(VENV)/bin/pre-commit

all: $(VENV) $(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL) $(PRESENTATION)

$(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL): %.pdf: docs/%.md
	sed 's|/assets|assets|g' $< | pandoc --output=$@ --from=markdown

$(PRESENTATION): %.pdf: docs/%.md
	sed 's|/assets|assets|g' $< \
		| pandoc $(PANDOC_OPTS) --output=$@ --from=markdown --to=beamer

.PHONY: archive
archive: $(ARCHIVE)

$(ARCHIVE): $(REPORT) $(PRESENTATION) $(USER_MANUAL) $(INSTALLATION_MANUAL)
	git archive --output=$@ $(^:%=--add-file=%) HEAD

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --requirement requirements.txt

.PHONY: $(VENV)
$(VENV): $(VENV)/bin/activate

pre-commit: $(VENV)
	$(PRE_COMMIT) install

clean:
	rm -rf \
		$(VENV) \
		$(BUILD_DIR) \
		$(ARCHIVE) \
		$(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL) $(PRESENTATION)
	find . -type f -name '*.pyc' -delete

run: $(VENV)
	(sleep 1 && xdg-open "http://127.0.0.1:8080") &
	$(PYTHON) ./src/app.py
