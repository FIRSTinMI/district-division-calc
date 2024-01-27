import numpy
from dataclasses import dataclass

@dataclass
class DivisionTeam:
    team_number: int
    district_points: int

@dataclass
class Division:
    name: str
    teams: list[DivisionTeam]
    
    def strength(self) -> float:
        return numpy.average([team.district_points for team in self.teams]) # type: ignore
    
    @staticmethod
    def __snr(point_list: list[int]) -> float:
        return 10 * numpy.log10(numpy.average(point_list)**2 / numpy.std(point_list)**2)  # type: ignore
    
    def snr(self) -> float:
        return Division.__snr([team.district_points for team in self.teams])
    
    def top_snr(self) -> float:
        '''Calculates the signal-to-noise ratio of the top 25% of teams'''
        return Division.__snr([team.district_points for team in sorted(self.teams, key=lambda t: t.district_points)[:len(self.teams)//4]])