import os
import core

if __name__ == '__main__':
    core.main(
        "data/search_meguro.csv",
        "data/meguro.geojson",
        "Meguro-ku",
        {
            "CONSUMER_KEY":        os.getenv("MEGURO_CONSUMER_KEY"),
            "CONSUMER_SECRET":     os.getenv("MEGURO_CONSUMER_SECRET"),
            "ACCESS_TOKEN":        os.getenv("MEGURO_ACCESS_TOKEN"),
            "ACCESS_TOKEN_SECRET": os.getenv("MEGURO_ACCESS_TOKEN_SECRET"),
        },
    )
