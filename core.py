import datetime
import json
import random
import time

import geopandas as gpd
import pandas as pd
import requests
import requests_oauthlib
import shapely.geometry

def get_tweets(oauth, lat, lon, r):
    api = "https://api.twitter.com/1.1/search/tweets.json"

    geocode = "{},{},{}km".format(lat, lon, r)
    params = {"q": "", "geocode": geocode, "result_type": "recent", "count": 100}

    req = requests.get(api, auth=oauth, params=params)
    tweets_json = json.loads(req.content.decode("utf-8"))

    ret = pd.DataFrame()
    if "statuses" not in tweets_json:
        return ret

    for tw in tweets_json["statuses"]:
        ret = ret.append(
            pd.DataFrame({
                "following": tw["user"]["following"],
                "screen_name": tw["user"]["screen_name"],
                "user_id": tw["user"]["id"],
                "text": tw["text"],
                "id": tw["id"],
                "date": datetime.datetime.strptime(tw["created_at"], "%a %b %d %H:%M:%S %z %Y"),
                "location_name": tw["place"]["name"] if tw.get("place") else "",
                "coordinates": [tw["place"]["bounding_box"]["coordinates"][0]] if tw.get("place") else [],
            })
        )
    return ret

def get_follow_list(df_tweets, gdf_boundaries, location_name):
    df_tweets["coordinates"] = df_tweets["coordinates"].apply(shapely.geometry.Polygon)
    tmp_gdf_tweets = gpd.GeoDataFrame(df_tweets, geometry="coordinates")
    tmp_gdf_tweets["area"] = tmp_gdf_tweets.area
    tmp_gdf_tweets["centroid"] = tmp_gdf_tweets.centroid
    tmp_gdf_tweets["geometry"] = tmp_gdf_tweets["coordinates"]
    ar = tmp_gdf_tweets["area"] == 0
    tmp_gdf_tweets["geometry"][ar] = tmp_gdf_tweets["centroid"][ar]
    gdf_tweets = gpd.GeoDataFrame(tmp_gdf_tweets, geometry="geometry")

    gdf_tweets["contains"] = gdf_boundaries.contains(gdf_tweets)
    gdf_tweets["eq_name"] = gdf_tweets["location_name"] == location_name
    gdf_tweets["in_area"] = gdf_tweets["contains"] | gdf_tweets["eq_name"]
    gdf_area_tweets = gdf_tweets[gdf_tweets["in_area"]]
    gdf_area_tweets_none_following = gdf_area_tweets[gdf_area_tweets["following"] == 0]
    grouped = gdf_area_tweets_none_following.groupby("user_id")
    gr_max = grouped["screen_name", "date", "id", "location_name"].max()
    return gr_max.sort_values("date", ascending=False)

def follow(oauth, df_follow):
    print(df_follow)
    api = "https://api.twitter.com/1.1/friendships/create.json"
    for i, _ in df_follow.iterrows():
        params = {"user_id": i}
        req = requests.post(api, auth=oauth, params=params)
        print(req, req.content)
        time.sleep(60 * random.random())

def main(search_loc_file, boundaries_file, specific_loc_name, twitter_api_keys, top=10):
    k = twitter_api_keys
    oa = requests_oauthlib.OAuth1(
        k["CONSUMER_KEY"],
        k["CONSUMER_SECRET"],
        k["ACCESS_TOKEN"],
        k["ACCESS_TOKEN_SECRET"],
    )

    df_tweets = pd.DataFrame()
    df_search_meguro = pd.read_csv(search_loc_file)
    for _, r in df_search_meguro.iterrows():
        df_tweets = df_tweets.append(get_tweets(oa, r["latitude"], r["longitude"], r["radius_km"]))

    gdf_meguro = gpd.read_file(boundaries_file)
    df_follow = get_follow_list(df_tweets.head(top), gdf_meguro, specific_loc_name)

    follow(oa, df_follow)
