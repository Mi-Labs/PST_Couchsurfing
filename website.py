import os
import folium


def show_at_map(osm_ids, results, contact_dataset):
    """
    Show the data on the map
    :param osm_ids:             The ids of the contacts
    :param results:             The query results
    :param contact_dataset:     The dataset of all contacts
    :return:
    """
    osm_map = folium.Map(location=[51.879092, 9.640534], zoom_start=7.5)
    marker_list = []

    # Get the amenities
    for uid in osm_ids:
        if __debug__:
            print(f"(uid={uid}):")

        uid_result = results[uid]

        # Check if uid has no result
        if type(uid_result) == str:
            print(f"\t{results[uid]}")
        # Build Marker
        else:
            marker = build_uid_marker(uid_result)
            if marker is not None:
                marker_list.append(marker)

    # Get the contacts
    for contact in contact_dataset:
        name = contact[0]
        tel = contact[1]
        lat = contact[2][0]
        lon = contact[2][1]
        contact_marker = create_contact_marker(lat, lon, tel, name)
        marker_list.append(contact_marker)

    # Add all marker to map
    for marker in marker_list:
        marker.add_to(osm_map)

    folium.LayerControl().add_to(osm_map)
    template_folder = os.path.join(os.getcwd(), 'template/map.html')
    osm_map.save(template_folder)
    # webbrowser.open("map.html")


def build_uid_marker(uid_data):
    """
    Build a list with all uid marker
    :param uid_data:
    :return: List with all folium marker
    """
    marker = None
    for element in uid_data:
        # TODO: Build better condition for No Result
        if "No results" in element:
            break

        try:
            keys = element.keys()
            # Get longitude directly or from center
            if "lon" in keys:
                lon = element['lon']
            else:
                lon = element['center']['lon']

            # Get latitude directly or from center
            if "lat" in keys:
                lat = element['lat']
            else:
                lat = element['center']['lat']

            # Get file_path || Exception
            name = element["tags"]["file_path"]
            amenity = element["tags"]['amenity']

            icon = choose_icon(amenity)
            # TODO: Opening hours
            # TODO: Clickable link

            popup_data = ""
            try:
                website = element['tags']['website']
                popup_data = "Website: " + website
            except KeyError:
                popup_data = "<i>Error 404 keine Website hinterlegt </i>"
                if __debug__:
                    print('No website found')
            finally:
                marker = create_amenity_marker(lat, lon, icon, popup_data, name)

        except KeyError:
            # print("Element doesn't have dtags")
            print(
                f"\tError occured with element:{element}\n...likely doesn't have a file_path tagged")
    return marker


def create_contact_marker(lat, lon, tel, tooltip):
    """
    Set a contact marker with phone number
    :param lat:         The latitude for the marker
    :param lon:         The longitude for the marker
    :param tel:         The phone number of the contact
    :param tooltip:     The tooltip on hover
    :return:
    """
    marker = folium.Marker([lat, lon],
                           popup=folium.Popup("Tel: " + tel, parse_html=True, max_width=200),
                           tooltip=str(tooltip))
    return marker


def create_amenity_marker(lat, lon, icon, popup_data, tooltip):
    """
    Sets a folium marker with popup
    :param lat:         The latitude for the marker
    :param lon:         The longitude for the marker
    :param icon:        The icon for the marker
    :param popup_data:  The content of the popup
    :param tooltip:     The tooltip on hover
    :return:            Folium marker
    """
    marker = folium.Marker([lat, lon],
                           icon=folium.CustomIcon(icon, icon_size=(15, 15),
                                                  icon_anchor=(15, 15)),
                           popup=popup_data, tooltip=tooltip)
    return marker


def choose_icon(amenity):
    """
    Choose an icon for the given amenity
    # TODO: Do more different amenities
    :param amenity: The file_path of the amenity
    :return: Path to the icon
    """
    asset_folder = 'assets/icons'
    beer_locations = ["bar", "biergarten", "bus_station", "pub"]
    if amenity not in beer_locations:
        return None
    icon = 'bier.png'

    return asset_folder + '/' + icon
