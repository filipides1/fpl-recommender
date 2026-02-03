import requests
import json
import os
from groq import Groq

def fetch_fpl_data():
    """Fetch FPL data from the official API"""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    return response.json()

def filter_top_players(data):
    """Filter and prepare top performing players"""
    players = data['elements']
    
    # Sort by form and total points
    top_by_form = sorted(
        [p for p in players if p['minutes'] > 500],  # Players with significant game time
        key=lambda x: (float(x['form']), x['total_points']),
        reverse=True
    )[:30]
    
    # Prepare context for AI
    player_info = []
    teams = {team['id']: team['name'] for team in data['teams']}
    
    for player in top_by_form:
        info = {
            'name': player['web_name'],
            'team': teams[player['team']],
            'position': ['GKP', 'DEF', 'MID', 'FWD'][player['element_type'] - 1],
            'form': player['form'],
            'points': player['total_points'],
            'price': player['now_cost'] / 10,
            'selected_by': player['selected_by_percent']
        }
        player_info.append(info)
    
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
    prompt = f"""You are an expert Fantasy Premier League advisor. Based on this player data, provide recommendations in JSON format.

Player Data:
{json.dumps(players_data[:20], indent=2)}

Provide your response in this exact JSON format:
{{
  "gw_captain": "Player Name",
  "captain_reason": "Why this player is the best captain choice",
  "differential": "Player Name",
  "differential_reason": "Why this low-owned player could be valuable",
  "transfers_in": ["Player1", "Player2", "Player3"],
  "transfers_out": ["Reason1", "Reason2", "Reason3"],
  "general_advice": "Overall strategy for this gameweek"
}}

Focus on form, fixtures, and value. Keep it concise."""

    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
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
            "transfers_in": ["Form Player"],
            "transfers_out": ["Check manually"],
            "general_advice": "API temporarily unavailable"
        }

def save_picks(recommendations, output_path='../data/picks.json'):
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
