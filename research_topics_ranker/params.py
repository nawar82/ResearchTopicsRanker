import os



##################  VARIABLES  ##################
QUERY = os.environ.get("QUERY")
EUTILS_API_KEY = os.environ.get("EUTILS_API_KEY")
EMAIL = os.environ.get("EMAIL")

##################  CONSTANTS  ##################
NR_OF_REQUESTS = int(os.environ.get("NR_OF_REQUESTS")) # type: ignore
