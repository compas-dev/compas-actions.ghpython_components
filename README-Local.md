## install

```bash
conda env create -f environment.yml
```

## create env_path.txt
1. Copy `env_path.txt.template` to `env_path.txt`
2. Edit the path in `env_path.txt` to your local conda environment site-packages path.

## develop

## componentize
```bash
conda activate gh_timber
python componentize_cpy.py components dist --version "0.1.0"
```

copy the generated files in `dist` to your Grasshopper userObjects folder.

## test

## Update

```bash
conda env update -f environment.yml
```