# SUEWS_parameters
Methods to calculate SUEWS related parameters

Currently investigated:

- Parameters related to LAI for vegetated surfaces
- Parameters related to Albedo for vegetated surfaces
- Parameters related to Surface Conductance for vegetated surfaces (g1-g6)


## dependencies
```
supy-driver 2019a18
supy   2019.11.24
pandas  0.25.3
```

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
