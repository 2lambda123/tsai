# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/073_wandb.ipynb.

# %% auto 0
__all__ = ['get_wandb_agent', 'run_wandb_agent', 'wandb_agent', 'update_run_config', 'check_config_sweep']

# %% ../nbs/073_wandb.ipynb 3
import warnings
from .imports import *
from fastcore.script import *
from .utils import *
from .export import *

# %% ../nbs/073_wandb.ipynb 4
def wandb_agent(script_path, sweep, entity=None, project=None, count=None, run=True):
    "Run `wandb agent` with `sweep` and `script_path"
    try: import wandb
    except ImportError: raise ImportError('You need to install wandb to run sweeps!')
    if 'program' not in sweep.keys(): sweep["program"] = script_path
    sweep_id = wandb.sweep(sweep, entity=entity, project=project)
    entity = ifnone(entity, os.environ['WANDB_ENTITY'])
    project = ifnone(project, os.environ['WANDB_PROJECT'])
    print(f"\nwandb agent {entity}/{project}/{sweep_id}\n")
    if run: wandb.agent(sweep_id, function=None, count=count)

get_wandb_agent = named_partial("get_wandb_agent", wandb_agent, run=False)

run_wandb_agent = named_partial("run_wandb_agent", wandb_agent, run=True)

# %% ../nbs/073_wandb.ipynb 5
def update_run_config(config, new_config, verbose=False):
    "Update `config` with `new_config`"
    config_dict = config.copy()
    for k, v in new_config.items():
        if k in config_dict.keys():
            if verbose:
                print(f"config.{k} {config_dict[k]} updated to {new_config[k]}")
            config_dict[k] = new_config[k]
        elif (
            hasattr(config_dict, "arch_config")
            and k in config_dict["arch_config"].keys()
        ):
            if verbose:
                print(
                    f"config.arch_config.{k} {config['arch_config'][k]} updated to {new_config[k]}"
                )
            config["arch_config"][k] = new_config[k]
        else:
            warnings.warn(f"{k} not available in config or config.arch_config")
    return config_dict

# %% ../nbs/073_wandb.ipynb 6
def check_config_sweep(config):
    "Checks if config has a sweep key and if so, checks if all sweep parameters are in config."
    sweep = config.get("sweep", {})
    if not sweep:
        return
    assert hasattr(sweep, "parameters")
    _config = config.copy()
    del _config["sweep"]
    for k, _ in sweep["parameters"].items():
        assert k in _config.keys() or (
            hasattr(config, "arch_config") and k in _config["arch_config"].keys()
        ), f"{k} is not a key in config"
