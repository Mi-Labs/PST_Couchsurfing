import helper_functions as hf
import pickle
import pandas as pd
import geo_coding
import osm
import website

temp_path = "temp/"


def unpickle_file(file):
    """
    Deserializes object from disk
    :param file:    The path of the object to deserialize
    :return:        The deserialized object
    """
    with open(file, 'rb') as f:
        return pickle.load(f)


def pickle_file(to_be_saved, file_path):
    """
    Serializes python object
    :param to_be_saved:  The object that should be saved
    :param file_path:    The file path (including filename)
    """
    with open(file_path, 'wb') as f:
        pickle.dump(to_be_saved, f, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    """
    Main program loop
    Gets data and returns map
    :return:
    """
    # Read contacts from csv
    df_contacts = pd.read_csv("Kontakte.csv")

    # Pickle results for quicker loading times
    pickled_files = {
        "id": temp_path + "osm_id.pkl",
        "contact": temp_path + "contact_coords.pkl",
        "result": temp_path + "results.pkl"
    }
    osm_ids_file = pickled_files.get("id")
    contact_coords_file = pickled_files.get("contact")
    results_file = pickled_files.get("result")

    if hf.check_file_exists(osm_ids_file):
        print('Unpickle osm ids and contact coords')
        osm_ids_contacts = unpickle_file(osm_ids_file)
        contact_coords = unpickle_file(contact_coords_file)
    else:
        contact_coords = geo_coding.get_contacts_base_info(df_contacts)
        osm_ids_contacts = geo_coding.get_osm_id_nearby_contacts(contact_coords)
        pickle_file(contact_coords, contact_coords_file)
        pickle_file(osm_ids_contacts, osm_ids_file)

    # Calculate places nearby
    if hf.check_file_exists(results_file):
        print('Unpickle search results')
        results = unpickle_file(results_file)
    else:
        results = osm.search_amenities_near_by(osm_ids_contacts)
        pickle_file(results, results_file)

    # Show on folium map
    website.show_at_map(osm_ids_contacts, results, contact_coords)
