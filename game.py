import random
import json
from datetime import datetime

class Team:
    def __init__(self, name, division, strength, budget):
        self.name = name
        self.division = division
        self.strength = strength
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.budget = budget
        self.goals_for = 0
        self.goals_against = 0

class BrazilianFootballManager:
    def __init__(self):
        self.teams = self.load_teams()
        self.current_season = 2024
        self.player_team = None
    
    def load_teams(self):
        # Real Brazilian teams with approximate strength ratings
        serie_a = [
            Team("Palmeiras", 1, 85, 50000000),
            Team("Flamengo", 1, 84, 45000000),
            Team("Fluminense", 1, 82, 35000000),
            Team("Grêmio", 1, 80, 30000000),
            Team("Atlético-MG", 1, 81, 32000000),
        ]
        
        serie_b = [
            Team("Sport", 2, 75, 15000000),
            Team("Vitória", 2, 74, 14000000),
            Team("Ceará", 2, 73, 13000000),
            Team("CRB", 2, 72, 12000000),
        ]
        
        serie_c = [
            Team("Paysandu", 3, 68, 5000000),
            Team("Amazonas", 3, 67, 4500000),
            Team("Brusque", 3, 66, 4000000),
            Team("Volta Redonda", 3, 65, 3500000),
        ]
        
        return serie_a + serie_b + serie_c

    def simulate_match(self, team1, team2):
        strength_diff = team1.strength - team2.strength
        base_chance = 50 + strength_diff
        
        team1_score = 0
        team2_score = 0
        
        for _ in range(random.randint(0, 5)):
            if random.randint(0, 100) < base_chance:
                team1_score += 1
            if random.randint(0, 100) < (100 - base_chance):
                team2_score += 1
        
        return team1_score, team2_score

    def play_match(self, team1, team2):
        score1, score2 = self.simulate_match(team1, team2)
        
        team1.goals_for += score1
        team1.goals_against += score2
        team2.goals_for += score2
        team2.goals_against += score1
        
        if score1 > score2:
            team1.points += 3
            team1.wins += 1
            team2.losses += 1
        elif score2 > score1:
            team2.points += 3
            team2.wins += 1
            team1.losses += 1
        else:
            team1.points += 1
            team2.points += 1
            team1.draws += 1
            team2.draws += 1
            
        return f"{team1.name} {score1} - {score2} {team2.name}"

    def start_game(self):
        print("=== Bem-vindo ao Brazilian Football Manager ===")
        print("\nEscolha seu time:")
        
        for i, team in enumerate(self.teams, 1):
            print(f"{i}. {team.name} (Série {team.division})")
        
        choice = int(input("\nDigite o número do time: ")) - 1
        self.player_team = self.teams[choice]
        print(f"\nVocê escolheu: {self.player_team.name}")
        
        self.play_season()

    def play_season(self):
        print(f"\n=== Temporada {self.current_season} ===")
        
        # Group teams by division
        divisions = {1: [], 2: [], 3: []}
        for team in self.teams:
            divisions[team.division].append(team)
        
        # Play matches in each division
        for division, teams in divisions.items():
            print(f"\nSérie {division}")
            for i, team1 in enumerate(teams):
                for team2 in teams[i+1:]:
                    result = self.play_match(team1, team2)
                    if team1 == self.player_team or team2 == self.player_team:
                        print(result)
        
        self.show_standings()
        self.handle_promotions_relegations()
        
    def show_standings(self):
        for division in [1, 2, 3]:
            print(f"\n=== Série {division} Classificação ===")
            teams_in_division = [t for t in self.teams if t.division == division]
            sorted_teams = sorted(teams_in_division, 
                                key=lambda x: (x.points, x.goals_for - x.goals_against), 
                                reverse=True)
            
            print("Time               | P  | J  | V  | E  | D  | GP | GC | SG")
            print("-" * 60)
            
            for team in sorted_teams:
                games = team.wins + team.draws + team.losses
                goal_diff = team.goals_for - team.goals_against
                print(f"{team.name:<18} | {team.points:2} | {games:2} | "
                      f"{team.wins:2} | {team.draws:2} | {team.losses:2} | "
                      f"{team.goals_for:2} | {team.goals_against:2} | {goal_diff:2}")

    def handle_promotions_relegations(self):
        # Implement promotion/relegation logic between divisions
        for division in [1, 2, 3]:
            teams_in_division = [t for t in self.teams if t.division == division]
            sorted_teams = sorted(teams_in_division, 
                                key=lambda x: (x.points, x.goals_for - x.goals_against), 
                                reverse=True)
            
            if division < 3:  # Relegation for Serie A and B
                sorted_teams[-1].division += 1
                sorted_teams[-2].division += 1
            
            if division > 1:  # Promotion for Serie B and C
                sorted_teams[0].division -= 1
                sorted_teams[1].division -= 1

if __name__ == "__main__":
    game = BrazilianFootballManager()
    game.start_game()