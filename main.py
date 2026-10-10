import nflreadpy as nfl
import pandas as pd
import numpy as np

def OPE_WOPR(): 
    current_season = nfl.get_current_season()
    stats = nfl.load_player_stats([current_season]).to_pandas()
    player_stats = stats[stats["position"].isin(["WR", "TE"])].copy()
    players_grouped = player_stats.groupby('player_display_name').agg({
        'team': 'last',
        'targets': 'sum',
        'receptions': 'sum',
        'receiving_yards': 'sum',
        'target_share': 'mean',
        'air_yards_share': 'mean',
        'week': 'count',
        'fantasy_points_ppr': 'mean'
    }).rename(columns={'week': 'Games'}).reset_index()

    players_grouped = players_grouped[players_grouped['targets'] >= 20]
    players_grouped['Catch Rate'] = players_grouped['receptions'] / players_grouped['targets']
    players_grouped['Yards/Target'] = players_grouped['receiving_yards'] / players_grouped['targets'] 
    players_grouped['Opportunity'] = (
        1.5 * players_grouped['target_share'].fillna(0) + 
        .5 * players_grouped['air_yards_share'].fillna(0)
)

    players_grouped['Efficiency'] = (
        players_grouped['Catch Rate'].fillna(0) *  (.1 * players_grouped['Yards/Target'])
        )
    team_pass_gp = stats.groupby('team').agg({'attempts': 'mean'}).reset_index()
    lg_avg_pass_gp = team_pass_gp['attempts'].mean()
    team_pass_gp['Pace'] = team_pass_gp['attempts'] / (lg_avg_pass_gp if lg_avg_pass_gp > 0 else 1)
    players_grouped = players_grouped.merge(team_pass_gp[['team', 'Pace']], on='team', how='left')
    players_grouped['Pace'] = players_grouped['Pace'].fillna(1.0)
    players_grouped['OPE-WOPR Score'] = (
        0.65 * players_grouped['Opportunity'] + 
        0.25 * players_grouped['Efficiency'] + 
        0.10 * players_grouped['Pace']
    )
    final_df = players_grouped.rename(columns={
        'player_display_name': 'Player',
        'team': 'Team',
        'targets': 'Targets',
        'Opportunity': 'Opportunity Score',
        'Efficiency': 'Efficiency Score',
        'target_share': 'Target share',
        'Yards/Target': 'Yards per Target',
        'receiving_yards': 'Yards',
        'Catch Rate': 'Catch%',
        'fantasy_points_ppr': 'PPR-Score-Avg'
        })
    final_df['PPR Rank'] = final_df['PPR-Score-Avg'].rank(ascending=False, method='min')
    final_df = final_df.sort_values(by='OPE-WOPR Score', ascending=False).reset_index(drop=True)
    final_df['OPE-Rank'] = range(1, len(final_df) + 1)
    cols = ['OPE-Rank', 'PPR Rank','Player', 'Team', 'PPR-Score-Avg', 'Opportunity Score', 'Efficiency Score', 'OPE-WOPR Score']
    top_75 = final_df.head(75)[cols].copy().round(3)
    filename = "OPE-WOPR.csv"
    top_75.to_csv(filename, index=False)
    print(f"printed {filename}")
    return top_75

if __name__ == "__main__":
    OPE_WOPR()