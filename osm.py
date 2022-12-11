# Fabi API info:
#   Die mit den id's zu ändernde / überschreibende Liste (bei mir set, damit id-Dopplungen von vornherein ausgeschlossen sind)
#   heißt <osm_ids>.
#
#   Die Ergebnisse sind in dem dict <results> nach key=uid.
#
#   Der Methodenaufruf <print_per_uid_ptty(file_path=True)> ist nicht notwendig und nur zur Veranschaulichung der erhaltenen Daten.
# ----------------------------------------------------------------------------------
# Todo bus in der nähe anzeigen Jeremie

import requests
import time

from requests import Response

results = {}  # dict<uid: query_result["elements"]>
error_codes = [429,400,504]

# todo amenity as param
def search_amenities_near_by(osm_id_list):
    """
    Searches amenities nearby the location
    :param osm_id_list: List with given osm ids (prefixed with type_)
    :return:  Dict with all osm results
    """
    print("Getting amenities nearby")
    overpass_url = "http://overpass-api.de/api/interpreter"
    init_search_radius = 500
    max_search_radius = 2000
    seconds_to_sleep = 2
    global results

    print(f"search_amenities_near_by(osm_id_list={osm_id_list})")
    include_searchplace = False  # should stay that way
    sp = ";nwr._->.res;out center;" if include_searchplace else "->.res;"

    print("Fetching Data...", end="\n" * 2)
    # For every osm id on the list
    for uid in osm_id_list:
        # Deconstruct modified uid
        deconstructed = uid.split('_')
        osm_type = deconstructed[0]
        osm_id = deconstructed[1]
        query_uid = build_uid_query(osm_type, osm_id)
        # resetting search_radius
        search_radius = init_search_radius

        while search_radius <= max_search_radius:
            if __debug__:
                print(f"For uid={osm_id}: sending query with radius={search_radius}")

            query = build_overpass_query(query_uid, sp, search_radius)

            response: Response = requests.get(overpass_url, params={"data": query})
            result = response.json()
            if response.status_code != 200:
                print(
                    f"Exception occured during data query: {response.status_code}"
                    + (
                        " (Too many requests)"
                        if response.status_code == 429
                        else " (Bad request)"
                        if response.status_code == 400
                        else " (Gateway Timeout)"
                        if response.status_code == 504
                        else " (unknown cause :)"
                    )
                )

            # dealing with empty result
            if result["elements"] == []:
                search_radius += 500  # expanding search radius
                time.sleep(seconds_to_sleep)
            else:
                time.sleep(seconds_to_sleep)
                break  # stops further querying

        results[uid] = (
            f"No results {search_radius}m near uid {uid} !"
            if result["elements"] == []
            else result["elements"]
        )

    return results


def build_uid_query(osm_type, uid):
    if osm_type is "w":
        return "way(id:" + uid + ")"
    elif osm_type is "n":
        return "node(id:" + uid + ")"
    else:
        return "relation(id:" + uid + ")"


def build_overpass_query(uid, sp, search_radius=500, include_shops=False):
    overpass_query = (
            f"[out:json][timeout:500];{uid}{sp}(nwr[amenity=bar](around.res:{search_radius});nwr[amenity=pub](around.res:{search_radius});nwr[amenity=biergarten](around.res:{search_radius});"
            + (
                f"nwr[shop=alcohol](around.res:{search_radius});nwr[shop=beverages](around.res:{search_radius}););"
                if include_shops
                else ");"
            )
            + "out center;"
    )
    return overpass_query
