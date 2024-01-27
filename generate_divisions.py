import typer
import sys
import random
from base64 import b64encode
from pathlib import Path

import models
import validate_divisions
import util

def main(
        api_key: str = typer.Option(..., help="Formatted as 'username:token'"),
        season: int = typer.Option(...),
        num_teams: int = typer.Option(..., help="The total number of teams to attend the championship"),
        district: str = typer.Option(..., help="FRC District Code"),
        divisions_file: Path = typer.Option(
            ...,
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True
        ),
        accommodations_file: Path = typer.Option(
            None,
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True
        ),
        out_file: Path = typer.Option(
            ...,
            file_okay=True,
            dir_okay=False,
            resolve_path=True
        ),
        force: bool = typer.Option(False),
        verbose: bool = typer.Option(False, "-v", help="Show extra debug messages")
):
    def print_debug(message: str):
        if verbose:
            typer.echo(typer.style(message, fg="cyan"))

    if not force and out_file.exists():
        raise typer.BadParameter("--out-file exists. Use --force to overwrite.")
    
    typer.echo("Generating divisions...")
    
    with open(divisions_file) as file:
        divisions = [line.rstrip() for line in file if line.rstrip()]
    if len(divisions) < 2:
        typer.echo("More than one division is required")
        raise typer.Exit(code=1)
    
    accommodations: dict[int, list[str]] = {}
    if accommodations_file is not None:
        with open(accommodations_file) as file:
            for line in file:
                tokens = line.rstrip().split(",")
                if len(tokens) < 2:
                    typer.echo(f"Accommodations for {tokens[0]} do not include any divisions")
                    raise typer.Exit(code=1)
                for division in tokens[1:]:
                    if division not in divisions:
                        typer.echo(f"Division {division} does not exist")
                        raise typer.Exit(code=1)
                accommodations[int(tokens[0])] = tokens[1:]
            
    quartile_size = num_teams // 4
    division_quartile_size = quartile_size // len(divisions)

    rankings = util.get_rankings(season, district, num_teams, api_key)

    # Divide into quartiles and shuffle them
    quartiles = [rankings[i * quartile_size:(i + 1) * quartile_size] for i in range(4)]

    while True:
        breaks_rule = False
        for quartile in quartiles:
            random.shuffle(quartile)
        # Use 10 teams from each quartile
        potential_divisions: list[models.Division] = []
        for i in range(len(divisions)):
            division_name = divisions[i]
            potential_divisions.append(models.Division(division_name, [team for chunk in quartiles for team in chunk[i*division_quartile_size:(i+1)*division_quartile_size]]))

        for division in potential_divisions:
            for team in division.teams:
                if team.team_number in accommodations:
                    if division.name not in accommodations[team.team_number]:
                        print_debug(f"Fails: accommodation for {team.team_number} not met (got {division.name}, need {accommodations[team.team_number]})")
                        breaks_rule = True
        
        if not validate_divisions.validate_divisions(potential_divisions):
            print_debug("Fails: Not within tolerances")
            breaks_rule = True
        if not breaks_rule:
            success_msg = " Successfully generated divisions! "
            typer.echo(typer.style("-"*len(success_msg), fg="green"))
            typer.echo(typer.style(success_msg, fg="green"))
            typer.echo(typer.style("-"*len(success_msg), fg="green"))
            break

    with open(out_file, "w") as file:
        for division in potential_divisions:
            file.write(f"{division.name}\n")
            for team in sorted([t.team_number for t in division.teams]):
                file.write(f"{team}\n")
            file.write(f"\n")

if __name__ == "__main__":
    assert sys.version_info >= (3, 7)
    typer.run(main)