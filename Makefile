BUILD_DIR = build

ARCHIVE             = BD-PL9-JoãoAlves-LuísGóis-MarcoSilva.zip
FLASK_OPTS          = --app src/app.py --env-file .env
ENV_FILE            = ./.env
FLASK_RUN_OPTS      = --debug --host "$$SERVER_HOST" --port "$$SERVER_PORT" --with-threads
INSTALLATION_MANUAL = installation-manual.pdf
OPEN                = xdg-open
PRESENTATION        = presentation.pdf
REPORT              = relatorio.pdf
USER_MANUAL         = user-manual.pdf
PANDOC_DATA_DIR     = pandoc
PANDOC_OPTS         = \
		      --variable=theme:Warsaw \
		      --highlight-style=assets/onehalfdark.theme

VENV        = venv
FLASK      := ./$(VENV)/bin/flask
PIP        := ./$(VENV)/bin/pip
PRE_COMMIT := ./$(VENV)/bin/pre-commit
PYTHON     := ./$(VENV)/bin/python3

ifneq ($(wildcard $(PANDOC_DATA_DIR)),)
	PANDOC_OPTS += \
		       $(foreach filter,\
		       $(wildcard $(PANDOC_DATA_DIR)/filters/*.lua),\
		       --lua-filter=$(filter))
endif

all: $(VENV) $(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL) $(PRESENTATION)

$(REPORT) $(USER_MANUAL) $(INSTALLATION_MANUAL): %.pdf: docs/%.md
	pandoc $(PANDOC_OPTS) --output=$@ $<

$(PRESENTATION): %.pdf: docs/%.md
	pandoc $(PANDOC_OPTS) --to=beamer --output=$@ $<

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

.PHONY: flask
flask: $(VENV)
	(. $(ENV_FILE) && $(FLASK) $(FLASK_OPTS) run $(FLASK_RUN_OPTS))

.PHONY: dev
dev: $(VENV)
	sudo docker compose up --detach
	sleep 3
	(. $(ENV_FILE) && $(OPEN) "http://$$SERVER_HOST:$$PGADMIN_DEFAULT_PORT")
	(. $(ENV_FILE) && sleep 1 && $(OPEN) "http://$$SERVER_HOST:$$SERVER_PORT") &
	(. $(ENV_FILE) && $(FLASK) $(FLASK_OPTS) run $(FLASK_RUN_OPTS))
	sudo docker compose stop
