FROM jupyter/datascience-notebook

USER ROOT

COPY environment.yml ${HOME}/environment.yml

# Add dependencies
RUN conda env update -f environment.yml --quiet && \
    rm -fr work environment.yml

# Add extensions
RUN jupyter labextension install \
    @jupyter-widgets/jupyterlab-manager \
    jupyterlab-plotly\
