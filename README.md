# SUEWS parameters
Methods to calculate SUEWS related parameters

Currently investigated:

- Parameters related to LAI for vegetated surfaces
- Parameters related to Albedo for vegetated surfaces
- Parameters related to Surface Conductance for vegetated surfaces (g1-g6)
- Parameters related to Surface Roughness and Zero Displacement height

## dependencies
Please look at `environment.yml`

## usage

1. set up the environment for running the notebooks:

```shell
conda create --file environments.yml
```

2. activate the `env` and install `ipykernel`

```shell
conda activate SUEWS_parameters
python -m ipykernel install --user --name SUEWS_parameters --display-name "SUEWS_prm"
```

3. launch jupyter notebooks

```
jupyter notebook
```

4. select kernel `SUEWS_prm`

## folders

- `data`: contains data needed to run modules
- `outputs`: contains outputs of the scripts
- `runs`: contains configuration for SUEWS runs

## files

- `*.ipynb`: main codes for testing parameters for SUEWS run for different surface type (name indicate the surface type)
- `*.py`: necessary modules for running `ipynb` files
- `all_attrs.csv`: contains the values of parameters used in the runs (change this if you want to test for different parameters)
- `site_info.csv`: contains information for the sites used in this repo

## data and references

data that are used from various resources:

1. AmeriFlux sites: https://ameriflux.lbl.gov/ (data in this repo)
2. AsiaFlux sites: http://www.asiaflux.net/ (need to be requested, not available in this repo)
3. Rice and wheat rice in Dongtai, China: `Duan, Z., Grimmond, S., Zhiqui, G., Sun, T., Liu, C. and Li, Y.: Radiation, energy, CO2 fluxes and energy balance closure over rice-wheat rotation: diurnal, seasonal and interannual (2014-2017) variations (under review), Agric. For. Meteorol., 2020` (need to be requested, not available in this repo)
