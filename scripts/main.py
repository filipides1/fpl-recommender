import requests
import json
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_fpl_data():
    """Fetch FPL data from the official API"""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    return response.json()

def filter_top_players(data):
    """Filter and prepare top performing players by position"""
    players = data['elements']
    teams = {team['id']: team['name'] for team in data['teams']}
    
    # Filter players by position with minimum game time
    positions = {
        'GKP': [p for p in players if p['element_type'] == 1 and p['minutes'] > 300],
        'DEF': [p for p in players if p['element_type'] == 2 and p['minutes'] > 500],
        'MID': [p for p in players if p['element_type'] == 3 and p['minutes'] > 500],
        'FWD': [p for p in players if p['element_type'] == 4 and p['minutes'] > 500]
    }
    
    # Get top players per position
    player_info = {}
    for pos_key, pos_players in positions.items():
        sorted_players = sorted(
            pos_players,
            key=lambda x: (float(x['form']), x['total_points']),
            reverse=True
        )
        
        # Get more players per position for better AI selection
        count = {'GKP': 10, 'DEF': 20, 'MID': 25, 'FWD': 15}
        top_for_position = sorted_players[:count[pos_key]]
        
        player_info[pos_key] = [
            {
                'name': p['web_name'],
                'team': teams[p['team']],
                'position': pos_key,
                'form': p['form'],
                'points': p['total_points'],
                'price': p['now_cost'] / 10,
                'selected_by': p['selected_by_percent']
            }
            for p in top_for_position
        ]
    
    return player_info

def get_ai_recommendations(players_data):
    """Get AI recommendations using Groq"""
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("Warning: GROQ_API_KEY not found. Using mock data.")
        return {
            "gw_captain": "Haaland",
            "captain_reason": "Top scorer with excellent fixtures",
            "differential": "Mbeumo",
            "differential_reason": "Low ownership but consistent returns",
            "transfers_in": ["Salah", "Saka"],
            "transfers_out": ["Injured Player", "Suspended Player"],
            "general_advice": "Focus on form over fixtures this week"
        }
    
    client = Groq(api_key=api_key)
    
    # Create prompt
    prompt = f"""You are an expert Fantasy Premier League advisor. Based on this player data organized by position, provide recommendations in JSON format.

Player Data by Position:
Goalkeepers: {json.dumps(players_data['GKP'][:5], indent=2)}
Defenders: {json.dumps(players_data['DEF'][:10], indent=2)}
Midfielders: {json.dumps(players_data['MID'][:12], indent=2)}
Forwards: {json.dumps(players_data['FWD'][:8], indent=2)}

Provide your response in this exact JSON format:
{{
  "gw_captain": "Player Name",
  "captain_reason": "Why this player is the best captain choice",
  "differential": "Player Name",
  "differential_reason": "Why this low-owned player could be valuable",
  "transfers_in": {{
    "GKP": [{{"name": "Goalkeeper", "team": "Team", "reason": "Why"}}],
    "DEF": [{{"name": "Defender1", "team": "Team", "reason": "Why"}}, {{"name": "Defender2", "team": "Team", "reason": "Why"}}, {{"name": "Defender3", "team": "Team", "reason": "Why"}}, {{"name": "Defender4", "team": "Team", "reason": "Why"}}],
    "MID": [{{"name": "Midfielder1", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder2", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder3", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder4", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder5", "team": "Team", "reason": "Why"}}],
    "FWD": [{{"name": "Forward1", "team": "Team", "reason": "Why"}}, {{"name": "Forward2", "team": "Team", "reason": "Why"}}]
  }},
  "transfers_out": {{
    "GKP": [{{"name": "Goalkeeper", "team": "Team", "reason": "Why"}}],
    "DEF": [{{"name": "Defender1", "team": "Team", "reason": "Why"}}, {{"name": "Defender2", "team": "Team", "reason": "Why"}}, {{"name": "Defender3", "team": "Team", "reason": "Why"}}, {{"name": "Defender4", "team": "Team", "reason": "Why"}}],
    "MID": [{{"name": "Midfielder1", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder2", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder3", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder4", "team": "Team", "reason": "Why"}}, {{"name": "Midfielder5", "team": "Team", "reason": "Why"}}],
    "FWD": [{{"name": "Forward1", "team": "Team", "reason": "Why"}}, {{"name": "Forward2", "team": "Team", "reason": "Why"}}]
  }},
  "general_advice": "Overall strategy for this gameweek"
}}

IMPORTANT: 
- Recommend exactly: 1 GKP, 4 DEF, 5 MID, 2 FWD for BOTH transfers_in and transfers_out
- Use actual player names and teams from the provided data
- For transfers_in: Choose players in excellent form with good fixtures
- For transfers_out: Choose players losing form, injured, or with bad fixtures
- Keep reasons brief (one sentence each)
- Total: 12 players in, 12 players out

Focus on form, fixtures, and value."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        # Return mock data on error
        return {
            "gw_captain": "Haaland",
            "captain_reason": "API Error - Using default recommendation",
            "differential": "Mbeumo",
            "differential_reason": "Low ownership option",
            "transfers_in": {
                "GKP": [{"name": "Check manually", "team": "TBD", "reason": "API error"}],
                "DEF": [{"name": "Check manually", "team": "TBD", "reason": "API error"}] * 4,
                "MID": [{"name": "Check manually", "team": "TBD", "reason": "API error"}] * 5,
                "FWD": [{"name": "Check manually", "team": "TBD", "reason": "API error"}] * 2
            },
            "transfers_out": {
                "GKP": [{"name": "Check manually", "team": "TBD", "reason": "API error"}],
                "DEF": [{"name": "Check manually", "team": "TBD", "reason": "API error"}] * 4,
                "MID": [{"name": "Check manually", "team": "TBD", "reason": "API error"}] * 5,
                "FWD": [{"name": "Check manually", "team": "TBD", "reason": "API error"}] * 2
            },
            "general_advice": "API temporarily unavailable"
        }

def save_picks(recommendations, output_path='../public/picks.json'):
    """Save recommendations to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(recommendations, f, indent=2)
    print(f"✅ Picks saved to {output_path}")

def main():
    print("🔄 Fetching FPL data...")
    fpl_data = fetch_fpl_data()
    
    print("📊 Filtering top players...")
    top_players = filter_top_players(fpl_data)
    
    print("🤖 Getting AI recommendations...")
    recommendations = get_ai_recommendations(top_players)
    
    print("💾 Saving picks...")
    save_picks(recommendations)
    
    print("✅ Done! Recommendations ready.")

if __name__ == "__main__":
    main()
