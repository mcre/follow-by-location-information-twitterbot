import geopandas as gpd

# wget --no-check-certificate https://github.com/dataofjapan/land/raw/master/tokyo.geojson

if __name__ == '__main__':
    df = gpd.read_file("data/tokyo.geojson")
    df_meguro = df[df["code"] == 131105]
    print(df_meguro)
    df_meguro.to_file("data/meguro.geojson", driver="GeoJSON")
