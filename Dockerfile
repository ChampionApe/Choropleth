FROM jupyter/datascience-notebook

COPY .${HOME}

USER ROOT

RUN fix-permissions ${HOME}

RUN if [-e environment.yml ]; then \
        conda env update -f environment.yml;\
    fi
    
# Add extensions
RUN jupyter labextension install \
    @jupyter-widgets/jupyterlab-manager \
    jupyterlab-plotly\
