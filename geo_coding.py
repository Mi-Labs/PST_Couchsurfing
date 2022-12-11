from geopy.geocoders import Nominatim
import time


def get_osm_id_nearby_contacts(contact_base_info):
    """
    Returns a list of osm_ids with on id near each contact
    :param contact_base_info:
    :return:
    """
    if __debug__:
        print('Searching for id on coordinates')

    # Request object for nominatim
    locator = Nominatim(user_agent="myGeocoder")

    # Get the next id near the contact
    osm_id_list = []
    for contact in contact_base_info:
        lat = contact[2][0]
        lon = contact[2][1]
        location = locator.reverse([lat, lon])
        modded_uid = create_modified_osm_id(location.raw['osm_type'], location.raw['osm_id'])
        time.sleep(2)
        osm_id_list.append(modded_uid)

        if __debug__:
            print('Name: ' + contact[0])
            print(location.raw)

    return osm_id_list


def create_modified_osm_id(osm_type, uid):
    """
    Prefixes the osm_id with the type for better queries later
    :param osm_type:    The type of the osm_id
    :param uid:         The osm_id
    :return:            Prefixed osm_id , e.g. w_1234567 or n_23452
    """
    print(osm_type)
    if osm_type == "way":
        prefix = 'w'
    elif osm_type == "node":
        prefix = 'n'
    else:
        prefix = 'r'

    return prefix + '_' + str(uid)


def get_contacts_base_info(contact_df):
    """
    Returns address, coordinates and phone number for every contact in dataframe
    :param contact_df: The dataframe from the phonebook
    :return:
    """
    if __debug__:
        print('Reading contact information')
    i = 0
    nominatim = Nominatim(user_agent="GetLoc")
    base_information_list = []

    while i < contact_df.shape[0]:
        # Get the address
        postcode = contact_df.loc[i].get('Plz')
        ort = contact_df.loc[i].get('Ort')
        street = contact_df.loc[i].get('Street')
        house_number = contact_df.loc[i].get('Hausnummer')
        adresse = ort + ' ' + str(postcode).split('.')[0] + ' ' + street + ' ' + str(house_number).split('.')[0]

        # Get the coordinates
        coords = nominatim.geocode(adresse, timeout=10)
        time.sleep(2)
        # liest geo daten aus
        if __debug__:
            print(coords)

        base_information_list.append(
            (contact_df.loc[i].get('Name'),
             contact_df.loc[i].get('Tel'),
             (coords.latitude, coords.longitude)
             )
        )  # liste mit Namen, Tel und Koordinaten
        if __debug__:
            print("Latitude = ", coords.latitude, "\n")
            print("Longitude = ", coords.longitude)
            print(base_information_list)

        i = i + 1
    return base_information_list
