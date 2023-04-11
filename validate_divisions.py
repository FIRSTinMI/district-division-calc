import typer
import sys
from pathlib import Path
import models

def within_tolerance(val_list: list[float], tolerance: float):
    return max(val_list) - min(val_list) <= tolerance

def validate_divisions(division_output: list[models.Division]) -> bool:
    if not within_tolerance([d.strength() for d in division_output], 2):
        return False
    if not within_tolerance([d.snr() for d in division_output], 2.5):
        return False
    if not within_tolerance([d.top_snr() for d in division_output], 2):
        return False
    return True

def main(out_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True, readable=True)):
    print("Separate validation script to be completed")

if __name__ == "__main__":
    assert sys.version_info >= (3, 7)
    typer.run(main)