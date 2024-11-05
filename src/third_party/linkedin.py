import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()


def scrape_linkedin_profile(linkedin_url: str = "", mock: bool = False):
    """
    Scrap information from LinkedIn profiles,
    manually scrpae the infroamtion from the linkedin profile
    """
    linkedin_json = get_linkedin_json_str(linkedin_url, mock)
    return linkedin_json


def get_linkedin_json_str(linkedin_url, mock):
    linkedin_json_str = None
    if mock is True:
        with open("james_linkedin.json", 'r') as file:
            linkedin_json = json.load(file)
            linkedin_json_str = simplify_linkedin_json_str(json.dumps(linkedin_json))

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        api_key = os.environ["PROXY_CURL"]
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {"url": linkedin_url}

        res = requests.get(url=api_endpoint,
                           params=params,
                           headers=headers)

        linkedin_json_str = simplify_linkedin_json_str(res._content.decode("utf-8"))
    return linkedin_json_str


def simplify_linkedin_json_str(json_str: str):
    dict = json.loads(json_str)
    dict_ = dict.copy()

    for (k, v) in dict.items():
        if isinstance(v, list) and len(v) == 0:
            dict_.pop(k, None)
        if v is None:
            dict_.pop(k, None)

    dict_.pop("people_also_viewed", None)
    dict_.pop("similarly_named_profiles", None)
    simplified_str = json.dumps(dict_)
    return simplified_str


if __name__ == "__main__":
    data = scrape_linkedin_profile(mock=True)
    print(data)
