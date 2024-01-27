import typer
import sys
import os
import numpy
from pathlib import Path

import models
import util

CHECK_MARK = "✅"
X_MARK = "❌"

def __within_tolerance(val_list: list[float], tolerance: float):
    return max(val_list) - min(val_list) <= tolerance

def validate_divisions(division_output: list[models.Division]) -> bool:
    '''Checks that divisions conform with the tolerances set in the FRC game manual'''
    if not __within_tolerance([d.strength() for d in division_output], 2):
        return False
    if not __within_tolerance([d.snr() for d in division_output], 2.5):
        return False
    if not __within_tolerance([d.top_snr() for d in division_output], 2):
        return False
    return True

def main(
    out_file: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True, readable=True),
    api_key: str = typer.Option(..., help="Formatted as 'username:token'"),
    season: int = typer.Option(...),
    district: str = typer.Option(..., help="FRC District Code"),
):
    typer.echo("NOTE: this tool assumes that all constraints from accommodations have been fulfilled")

    team_mapping: dict[str, list[int]] = {}
    with open(out_file) as file:
        for block in file.read().strip().split(os.linesep+os.linesep):
            lines = block.splitlines()
            if len(lines) < 2:
                typer.echo("Division does not have any teams listed. Failing.", err=True)
                raise typer.Exit(code=1)
            name = lines[0]
            team_mapping[name] = [int(line) for line in lines[1:]]

    rankings = util.get_rankings(season, district, sum([len(v) for v in team_mapping.values()]), api_key)
    team_rankings_map = {team.team_number: team for team in rankings}

    divisions = [models.Division(k, [team_rankings_map[t] for t in v]) for (k, v) in team_mapping.items()]
    
    # Check that the math works out
    is_valid = validate_divisions(divisions)
    if is_valid:
        typer.echo(typer.style(f"{CHECK_MARK} Divisions are within game manual tolerances", fg="green"))
    else:
        typer.echo(typer.style(f"{X_MARK} Divisions are NOT within game manual tolerances", fg="red"))

    # Make sure each team is only on one division, once
    teams, counts = numpy.unique([t.team_number for d in divisions for t in d.teams], return_counts=True)
    duplicate_teams = teams[counts > 1]
    if len(duplicate_teams) == 0:
        typer.echo(typer.style(f"{CHECK_MARK} No duplicate teams", fg="green"))
    else:
        typer.echo(typer.style(f"{X_MARK} Duplicate teams: {', '.join([str(t) for t in duplicate_teams])}", fg="red"))


if __name__ == "__main__":
    assert sys.version_info >= (3, 7)
    typer.run(main)