def pandas2geopandas(df):
    # a function to convert a pandas data frame to geopandas data frame
    geometries = [shapely.geometry.Point(xy) for xy in zip(df.lng, df.lat)]
    crs = {'init': 'epsg:4326'}
    gf = gpd.GeoDataFrame(df, crs=crs, geometry=geometries)
    return(gf)

def test_conversion():
    # test the first coordinate of the conversion
    d = {'place_id':[1,2,3],'lat':[47.615866, 47.618850, 47.596843],'lng':[-122.309913, -122.325005, -122.326929]}
    df = pd.DataFrame(d)
    res = gpd_tools.pandas2geopandas(df)
    assert(res.place_id[0] == df.place_id[0])


def convex_hull_shape(gf):
    point_collection = shapely.geometry.MultiPoint(gf.geometry.tolist())
    polygon = point_collection.convex_hull
    gfShape = gpd.GeoDataFrame(geometry=[polygon], crs = {'init': 'epsg:4326'})
    return(gfShape)



def places_per_neighborhood(gfN, gf, neighborhood):
    gfNeighborhood = gfN.query('nhood == @neighborhood')
    nhood_places = gpd.sjoin(gf, gfNeighborhood, how="inner", op='within')
    return(nhood_places)
