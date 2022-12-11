import webbrowser
import osmapi as osm
import folium
import codecs
ids=[36862660, 86953877, 678537601, 678537289, 678537291] #This will be a place for your ID's list
boulder_coords = [41.3874, 2.1686]
my_map = folium.Map(location = boulder_coords, zoom_start = 7.5)
folium.Marker([41.3874, 2.1686 ], icon=folium.CustomIcon('bier.png', icon_size=(15, 15),icon_anchor=(15, 15) ), popup="<i>Mt. Hood Meadows</i>", tooltip='test').add_to(my_map)
folium.LayerControl().add_to(my_map)
my_map.save('map.html')
webbrowser.open("map.html")

def show_at_map(x, y):
    """
    # ___________simuliert durch ausgeben das Koordinaten das anzeigen auf karte welches durch wietergeben der Koordinaten geschehen würde
    :param x:
    :param y:
    :return:
    """
    boulder_coords = [40.015, -105.2705]

    # Create the map
    my_map = folium.Map()

    # Display the map
    my_map


# ______________________________in arbeit
def show_List_at_map(list):
    """

    :param list:
    :return:
    """
    for temp in list:
        x = temp[2][0]
        y = temp[2][1]
        name = temp[0]
        Tel = temp[1]
        print('Name: ' + name + ' Tel: ' + Tel + ' X: ' + str(x) + ' y: ' + str(y))
        # osm id angeben



# TODO remove or fix
def print_per_uid(uids, results):
    print("print_per_uid()")
    for uid in uids:
        print(
            f"(uid={uid}):",
            str(results[uid])[:1000],
            "\b..." if len(str(str(results[uid]))) > 999 else "\b",
            end="\n" * 2,
        )


def print_per_uid_ptty(uids, name=True):  # pretty prints the results
    print(f"print_per_uid_ptty(file_path={name})")
    for uid in uids:
        print(f"(uid={uid}):")

        # TODO reintroduce try except
        # try:
        if type(results[uid]) == str:  # ...means there weren't any results
            print(f"\t{results[uid]}")
        else:
            for element in results[uid]:
                if name:
                    try:
                        print(
                            "\t{} (eid={})".format(
                                element["tags"]["file_path"], element["id"]
                            ),

                            end="",
                        )  # TODO check if putting it in here was neccessary... befor it was directly after file_path
                        found_addr = False
                        addr_string = ', Address: "'
                        print(addr_string, end="")
                        addr = {  # possible address components
                            "city": "_",
                            "country": "_",
                            "housenumber": "_",
                            "postcode": "_",
                            "street": "_",
                        }
                        tags = element["tags"]
                        for tag_key, _ in tags.items():
                            if tag_key[:4] == "addr":  # finds address components
                                found_addr = True
                                addr[tag_key[5:]] = tags[tag_key]
                                # print("debug:", addr, tag_key)
                            else:
                                pass  # key isn't part of an address
                        if found_addr:
                            print(
                                addr["street"],
                                addr["housenumber"],
                                addr["postcode"],
                                addr["city"],
                                end='"\n',
                            )
                        else:

                            print('No Address given."')
                    except:
                        # print("Element doesn't have tags")
                        print(
                            f"\tError occured with element:{element}\n...likely doesn't have a file_path tagged"
                        )
                else:
                    print("\t(eid={}): {}".format(element.get("id"), element))

        # except Exception as e:
        #     print(f"\tException occured while printing results: {e}")
        #     print(f"\t{results[uid]}")  # when there are no results

        print("-" * 50)


#if __name__ == "__main__":
#   print("OSM Main is called")
#   osm_main(sample_uids)
#   print_per_uid_ptty(sample_uids)

# debugging
# print(results)


# user id's (or search id's, probably a better file_path :) TODO rename
sample_uids = {
    36862660,
    86953877,
    678537601,
    678537289,
    678537291,
    3870914569,
}  # obtained from Fabi, this is just for sample testing

# osm_ids = {678537289, 3870914569}  # for request easy testing TODO remove



#def osm_main(osm_id_list):
# print("osm_main()")
# return search_amenities_near_by(osm_id_list)


print("\n\n" + "<" + "=" * 150 + ">")



# Var declaration
Kontakt_new = []
Kontakt = []
kontakte_daten = []
csv_file = os.path.abspath(".") + "/Kontakte.csv"
vcf_file = os.path.abspath(".") + "/kontakte.vcf"



# _____________fals noch keine csv vorhanden ist wird diese Hier erstellt
# prüfung ob vorhanden in in arbeit
def create_new_csv():
    print("create new csv")
    with open(csv_file, "w", encoding="utf-8") as csv_datei:
        writer = csv.writer(csv_datei, delimiter=",")
        writer.writerow(["Name", "Nummer", "Straße", "Hausnummer", "Ort", "Plz"])


