# OpenSky Datashader

TODO: description


## Installation

The best way to install all the dependencies for this notebook is to create a conda environment. Either Miniconda or Anaconda are good.

You can use the `environment.yml` file included in this repository to create a conda environment identical to the one I used:

```sh
conda env create --file environment.yml
```

Otherwise you can create and activate a new conda environment with:

```sh
conda create --name opensky-datashader python=3.6 --yes
source activate opensky-datashader
```

And install all the dependencies with:

```sh
conda install -c bokeh datashader --yes
conda install -c conda-forge requests holoviews sqlalchemy sqlite cartopy --yes
```


## Data
https://opensky-network.org/


## Tests

```sh
pytest -v --cov=scripts/ --cov-report=term-missing
```


## Other
You can freeze your environment with:

```sh
conda env export > environment.yml
```

To remove this conda environment, run:

```sh
conda env remove -n geopython-2018
```


## See also:
https://anaconda.org/jbednar/opensky/notebook
