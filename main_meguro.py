import core

def handler(event, context):
    core.main(
        "data/search_meguro.csv",
        "data/meguro.geojson",
        "Meguro-ku",
    )
