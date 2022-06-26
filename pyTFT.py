import requests
from threading import Thread

__errors = {
    400 : "Bad request",
    401 : "Unauthorized",
    403 : "Forbidden",
    404 : "Data not found",
    405 : "Method not allowed",
    415 : "Unsupported media type",
    429 : "Rate limit exceeded",
    500 : "Internal server error",
    502 : "Bad gateway",
    503 : "Service unavailable",
    504 : "Gateway timeout"}

def get_data() -> dict:
    """Complete api documentation: "https://developer.riotgames.com/docs/portal"
    
    Returns:
        dict: All API constants
    """
    
    data = {}
    data["servers"] = ("BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1", "TR1", "RU")
    data["regions"] = ("AMERICAS", "ASIA", "EUROPE")
    data["errors"] = __errors
    data["tiers"] = ("DIAMOND", "GOLD", "SILVER", "BRONZE", "IRON", "PLATINUM")
    data["divisions"] = ("I", "I", "III", "IV")
    data["queue"] = ("RANKED_TFT_TURBO", )
    
    return data

def error_handle(status_code: int):
    """Internal function that controls the different errors in all requests

    Args:
        status_code (int): Request.status_code

    Raises:
        Exception: An exception pops up with the name of the error
    """
    
    for i in __errors:
        if i == status_code: raise Exception(f"{i}-{__errors[i]}")

def get_summoner_by_name(name_player: str, server_name: str, api_key: str) -> dict:
    """Direct call to /lol/summoner/v4/summoners/by-name/{name_player}
    
    Args:
        name_player (str): League of Legends player name
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key

    Returns:
        dict: Summoner
    
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name_player}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
        
    return call.json()

def get_summoner_by_puuid(encrypted_puuid: str, server_name: str, api_key: str) -> dict:
    """Direct call to /tft/summoner/v1/summoners/by-puuid/{encrypted_puuid}

    Args:
        encrypted_puuid (str): Puuid associated to the player obtained by some get_summoner()
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key

    Returns:
        dict: Summoner
        
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{encrypted_puuid}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
        
    return call.json()

def get_summoner_by_account_id(encrypted_account_id: str, server_name: str, api_key: str) -> dict:
    """Direct call to /tft/summoner/v1/summoners/by-account/{encrypted_account_id}

    Args:
        encrypted_account_id (str): AccountId associated to the player obtained by some get_summoner()
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key

    Returns:
        dict: Summoner
        
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/summoner/v1/summoners/by-account/{encrypted_account_id}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
        
    return call.json()

def get_summoner_by_summoner_id(encryptencrypted_summoner_id: str, server_name: str, api_key: str) -> dict:
    """Direct call to /tft/summoner/v1/summoners/{encryptencrypted_summoner_id}

    Args:
        encrypted_account_id (str): AccountId associated to the player obtained by some get_summoner()
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key

    Returns:
        dict: Summoner
        
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/summoner/v1/summoners/{encryptencrypted_summoner_id}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
        
    return call.json()

def get_matches_by_puuid(puuid: str, region: str, api_key: str, n_games: int, start: int = 0, start_time: int = 0, end_time: int = 0) -> dict:
    """Direct call to /tft/match/v1/matches/by-puuid/{puuid}/ids
    
    Args:
        puuid (str): Puuid associated to the player obtained by some get_summoner()
        region (str): Region from this tuple: get_data()["regions"]
        api_key (str): API access key
        n_games (int): Number of games to be obtained
        start (int): Start index, defaults to 0
        optional start_time (int): Time in EPOCH where the search begins
        optional end_time (int): Time in EPOCH where search ends

    Returns:
        dict: list of match_ids
    
    """
    
    start_time = f"startTime={start_time}&" if start_time else ""
    end_time = f"endTime={end_time}&" if end_time else ""
    
    api_call = f"https://{region}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start={start}&{end_time}{start_time}count={n_games}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()

def get_match_by_match_id(save: list, match_id: str, region: str, api_key: str):
    """Direct call to /tft/match/v1/matches/{match_id}
    
    Args:
        save (list): This function is expected to be used with threads so instead of a return you have to pass a list to which the MatchDto will be added.
        match_id (str): Match identifier obtained by, get_matchs_tft()
        region (str): Region from this tuple: get_data()["regions"]
        api_key (str): API access key
    
    """
    
    api_call = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match_id}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    save.append(call.json())

def get_info_matches(matches: list[dict], region: str, api_key: str) -> list[dict]:
    """Concurrent call to the api via get_info_match() for each item returned by get_matchs_tft()
    
    Args:
        matchs (list[dict]): list of matches obtained by match_by_match_id()
        region (str): Region from this tuple: get_data()["regions"]
        key (str): API access key
        
    Returns:
        list[dict]: Information of all match_ids

    """
    
    threads_list = []
    data = []
    for i in range(len(matches)):
        new_thread = Thread(target = get_match_by_match_id, args = (data, matches[i], region, api_key))
        threads_list.append(new_thread)
        new_thread.start()
    
    for i in threads_list:
        i.join()
    
    return data

def get_league_master(server_name: str, api_key: str) -> dict:
    """Concurrent call to /tft/league/v1/master
    
    Args:
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key

    Returns:
        dict: list of master players of type LeagueList
    
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/league/v1/master"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()

def get_league_grandmaster(server_name: str, api_key: str) -> dict:
    """Concurrent call to /tft/league/v1/grandmaster
    
    Args:
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key

    Returns:
        dict: list of grandmaster players of type LeagueList
    
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/league/v1/grandmaster"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()

def get_league_challenger(server_name: str, api_key: str) -> dict:
    """Concurrent call to /tft/league/v1/challenger
    
    Args:
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key

    Returns:
        dict: list of challenger players of type LeagueList
    
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/league/v1/challenger"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()

def get_league_by_summoner(summoner_id: str, server_name: str, api_key: str) -> dict:
    """Concurrent call to /tft/league/v1/entries/by-summoner/{summoner_id}
    
    Args:
        server_name (str): Server from this tuple: get_data()["servers"]
        api_key (str): API access key
        summoner_id (str): Id associated to the player obtained by some get_summoner()

    Returns:
        dict: Information of a player in tft of type LeagueEntry
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()

def get_league_by_tier_division(tier: str, division: str, server_name: str, api_key: str, page: int = 1) -> dict:
    """Concurrent call to /tft/league/v1/entries/{tier}/{division}?page={page}
    
    Args:
        server_name (str): Server from this tuple: get_data()["servers"]
        tier (str): Tier from this tuple: get_data()["tiers"]
        division (str): Division from this tuple: get_data()["divisions"]
        api_key (str): API access key
        optional page(int): Index to search, by default in 

    Returns:
        dict: list of players of {tier}{division} of type LeagueEntry
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/league/v1/entries/{tier}/{division}?page={page}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()

def get_league_by_leagueid(league_id: str, server_name: str, api_key: str) -> dict:
    """Concurrent call to /tft/league/v1/leagues/{league_id}
    
    Args:
        server_name (str): Server from this tuple: get_data()["servers"]
        league_id (str): The UUID of the league obtained by some get_league()
        api_key (str): API access key

    Returns:
        dict: list of players of {league_id} of type LeagueList
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/league/v1/leagues/{league_id}"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()

def get_league_rated_ladders(queue: str, server_name: str, api_key: str) -> dict:
    """Concurrent call to /tft/league/v1/rated-ladders/RANKED_TFT_TURBO/top
    
    Args:
        server_name (str): Server from this tuple: get_data()["servers"]
        queue (str): Queue from this tuple: get_data()["queues"]
        api_key (str): API access key

    Returns:
        dict: list of players of type TopRatedLadderEntry
    
    """
    
    api_call = f"https://{server_name}.api.riotgames.com/tft/league/v1/rated-ladders/{queue}/top"
    call = requests.get(api_call, params={"api_key" : api_key})
    error_handle(call.status_code)
    
    return call.json()