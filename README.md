Info
---------------------------
Simple, direct and lightweight wrapper to all TFT related RIOT API calls.
This wrapper can be used directly in your code or use it as a base to create a higher level wrapper, it has no dependencies.
To fully understand this wrapper it is essential that you read the official documentation of the api: https://developer.riotgames.com/docs/portal


Example
---------------------------

    from TFT_API import *

    # Data
    key = "your key"
    API_CONSTANT = get_data()
    player = "liquid snoodyboo"
    euw_server = API_CONSTANT["servers"][2]
    eu_region = API_CONSTANT["regions"][2]
    na_server = API_CONSTANT["servers"][7]
    diamond = API_CONSTANT["tiers"][0]
    division1 = API_CONSTANT["divisions"][0]

    # Get information from a player
    player = get_summoner_by_name(player, euw_server, key)
    last_games_played = get_matches_by_puuid(player["puuid"], eu_region, key, n_games=10)
    get_player_ranked_info = get_league_by_summoner(player["id"], euw_server, key)

    # Get information about the items
    # get_info_matches uses Threads to get all games concurrently
    games_info = get_info_matches(last_games_played, eu_region, key)

    # Get information about the qualifiers
    all_masters_na = get_league_master(na_server, key)
    all_grandmaster_na = get_league_grandmaster(na_server, key)
    all_challenger_na = get_league_challenger(na_server, key)
    all_diamond_1_na = get_league_by_tier_division(diamond, division1, na_server, key)


Support
---------------------------
If you want to support the project you can propose your improvements or leave a star in the project.
