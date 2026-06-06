# ---------------------------------------------------
# PLAYLIST CONFIGURATION
# ---------------------------------------------------

# Map series names and content types to their playlist IDs

PLAYLIST_IDS = {
    "bhagwat_gita": "PLVDQPpANT_UH1vVyJvX3VoTzGmf16AfBX",
    "ai_story": "PLVDQPpANT_UEH0sS065yaWB7IWEDDQmak",
}

# ---------------------------------------------------
# GET PLAYLIST ID
# ---------------------------------------------------

def get_playlist_id(series_name):
    """
    Get playlist ID for a given series name
    """
    return PLAYLIST_IDS.get(series_name)
