import pulp
import pandas as pd

from app.configs import players

##############
# notables
# connor bedard C
# logan cooley C -- get 
# Devon levi G
# Adam fantily C



##############

players = players
cash_need_for_remaining_players = 2000000 * 5
salary_cap = 50800000 - cash_need_for_remaining_players

# 9 players taken from here, best players, average salary is prob 3 mil, get a couple of players for the last 5
# at 950k, 


# Create a binary variable for each player
player_vars = pulp.LpVariable.dicts("Player", range(len(players)), 0, 1, pulp.LpInteger)

# Create a PuLP problem
prob = pulp.LpProblem("HockeyTeamSelection", pulp.LpMaximize)

# # Objective function (e.g., maximize total points)
# prob += pulp.lpSum(player_vars[i] * players[i]["points"] for i in range(len(players)))

# Objective function (maximize total points and total goals)
weight_points = 1.0  # Adjust the weight based on the importance of points vs. goals
weight_goals = 1.0  # Adjust the weight based on the importance of points vs. goals

# Add both objectives to the objective function
prob += weight_points * pulp.lpSum(player_vars[i] * players[i]['points'] for i in range(len(players)))
prob += weight_goals * pulp.lpSum(player_vars[i] * players[i]['goals'] for i in range(len(players)))


# Constraints
prob += pulp.lpSum(player_vars[i] for i in range(len(players))) == 9  # Total players
prob += (
    pulp.lpSum(
        player_vars[i] for i in range(len(players)) if players[i]["position"] == "g"
    )
    == 2
)  # Goalies
prob += (
    pulp.lpSum(
        player_vars[i] for i in range(len(players)) if players[i]["position"] == "d"
    )
    == 4
)  # Defensemen
prob += (
    pulp.lpSum(
        player_vars[i] for i in range(len(players)) if players[i]["position"] == "c"
    )
    == 1
)  # Forwards

prob += (
    pulp.lpSum(player_vars[i] for i in range(len(players)) if players[i]["position"] == "lw")
) == 1
prob += (
    pulp.lpSum(player_vars[i] for i in range(len(players)) if players[i]["position"] == "rw")
) == 1

prob += (
    pulp.lpSum(player_vars[i] * players[i]["salary"] for i in range(len(players)))
    <= salary_cap
)  # Salary constraint

# Add a list of unique team names
unique_teams = set(player["team"] for player in players)

# Constraint: Select one player from each team
for team in unique_teams:
    prob += (
        pulp.lpSum(
            player_vars[i] for i in range(len(players)) if players[i]["team"] == team
        )
        == 1
    )

# Solve the optimization problem
prob.solve()

# Print the selected players
selected_players = [
    players[i] for i in range(len(players)) if player_vars[i].value() == 1
]
for player in selected_players:
    print(player)
total_sal = 0
for player in selected_players :

    total_sal += player['salary']
total_sal

remaining_sal = salary_cap - total_sal
print(remaining_sal)