# Credit for ROOTDIR implementation:
# kenorb (https://stackoverflow.com/users/55075/kenorb),
# How to get current relative directory of your Makefile?,
# URL (version: 2017-05-23): https://stackoverflow.com/a/35698978
ROOTDIR						=	$(abspath $(patsubst %/,%,$(dir $(abspath		\
								$(lastword $(MAKEFILE_LIST))))))

SHELL						=	/bin/sh

PROJNAME					=	data-visualization-demo

RM							=	rm
COPY						=	cp
FIND						=	find

CONDA						=	conda
CONDA_ENV_FILE				=	environment.yml

PY							?=	python3
PY_SETUP					=	setup.py
PY_SETUP_DOCS				=	build_sphinx

JUPYTER						=	jupyter
JUPYTERLAB_EXTENSIONS		=	jupyterlab_vim									\
								jupyterlab_bokeh								\
								jupyterlab_templates							\
								@jupyterlab/git									\
								@jupyterlab/github								\
								@jupyterlab/plotly-extension					\
								@mflevine/jupyterlab_html						\
								@jupyter-widgets/jupyterlab-manager				\
								jupyter-matplotlib								\
								@ryantam626/jupyterlab_code_formatter
JUPYTERLAB_SERVEREXTENSION	=	jupyterlab_templates							\
								jupyterlab_git									\
								jupyterlab_code_formatter

DATAVIZTOOL					=	dataviztool

CLEAN_FILES					=	build/											\
								*_cache/										\
								docs/_build/ 									\
								dist/											\
								.pytest_cache/									\
								*.egg-info/

define makefile_help
	@echo 'Makefile for the data visualization demo repository.                      '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make help                           display this message (default)     '
	@echo '                                                                          '
	@echo '   make build                          build everything needed to install '
	@echo '   make csv                            convert dft outputs into csv format'
	@echo '   make clean                          remove temporary and build files   '
	@echo '   make develop                        install project in development mode'
	@echo '   make docs                           generate documentation             '
	@echo '   make env                            create conda venv and install deps '
	@echo '   make sdist                          create a source distribution       '
	@echo '   make test                           run unit tests                     '
	@echo '                                                                          '
endef

define build_cleanup
	-$(RM) -rf $(CLEAN_FILES)
endef

define bands2csv
	$(DATAVIZTOOL) bands2csv -o data/csv/bands.csv								\
		-f BAND_S01_A0001.OUT.fe_1atom_elecstr_ntype.gz 200 nonmagnetic			\
		-f BAND_S01_A0001.OUT.fe_1atom_elecstr_ftype.gz 200 ferromagnetic		\
		data/dft
endef

define dos2csv
	$(DATAVIZTOOL) dos2csv -o data/csv/dos.csv									\
		-f TDOS.OUT.fe_1atom_elecstr_ntype.gz 1 nonmagnetic						\
		-f TDOS.OUT.fe_4atoms_elecstr_ftype.gz 4 ferromagnetic					\
		-f TDOS.OUT.fe_4atoms_elecstr_gtype.gz 4 g-type							\
		data/dft
endef

define pycache_cleanup
	$(FIND) -name "__pycache__" -type d -exec $(RM) -rf {} +
endef

define update_conda_env
	bash -lc "$(CONDA) env update --file $(CONDA_ENV_FILE)"
endef

define run_setup_py
	$(PY) ./$(PY_SETUP) $(1)
endef

define install_jupyterlab_extensions
	$(JUPYTER) labextension install $(1)
endef

define install_serverextension
	$(JUPYTER) serverextension enable --py $(1)
endef

help :
	$(call makefile_help)

build :
	$(call run_setup_py,build)

clean :
	$(call build_cleanup)
	$(call pycache_cleanup)

csv :
	$(call bands2csv)
	$(call dos2csv)

develop :
	$(call run_setup_py,develop)

docs :
	$(call run_setup_py,$(PY_SETUP_DOCS))

env :
	$(call update_conda_env)

labextensions :
	$(foreach extension,$(JUPYTERLAB_EXTENSIONS),$(call install_jupyterlab_extensions,$(extension));)

serverextensions :
	$(foreach serverextension,$(JUPYTERLAB_SERVEREXTENSION),$(call install_serverextension,$(serverextension));)

sdist :
	$(call run_setup_py,sdist)

test :
	$(call run_setup_py,test)

.PHONY : help build clean develop docs env csv
