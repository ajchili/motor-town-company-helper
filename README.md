# motor-town-company-helper

A simple Python script which helps reduce the _pain_ of managing a company within the game Motor Town. This script will automatically repair your company vehicles without you needing it manage it yourself.

## Setup

1. Install [uv](https://github.com/astral-sh/uv)
1. Run `uv sync`

## Running

1. Active the virtual environment ([docs](https://docs.astral.sh/uv/pip/environments/#using-a-virtual-environment))
1. Run `python main.py`

### Variables

| Variable Name     | Type  | Allowed Values                               | Default Value |
| ----------------- | ----- | -------------------------------------------- | ------------- |
| `PROMPT`          | `str` | `"True" \| "False"`                          | `"False"`     |
| `COMPANY_SIZE`    | `int` | `[1, 10]` (inclusive range between 1 and 10) | `7`           |
| `REPAIR_INTERVAL` | `int` | `[1, ∞)` (greater than or equal to 1)        | `15`          |

Environment variables can be specified before the run command, example `PROMPT=True COMPANY_SIZE=10 REPAIR_INTERVAL=20 python main.py`
