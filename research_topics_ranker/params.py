from dotenv import load_dotenv
import os
load_dotenv()




##################  VARIABLES  ##################
QUERY = os.environ.get("QUERY")
EUTILS_API_KEY = os.environ.get("EUTILS_API_KEY")
EMAIL = os.environ.get("EMAIL")
N_COMPONENETS = int(os.environ.get("N_COMPONENETS")) # type: ignore
MAX_ITER = int(os.environ.get("MAX_ITER")) # type: ignore


##################  CONSTANTS  ##################
NR_OF_REQUESTS = int(os.environ.get("NR_OF_REQUESTS")) # type: ignore
