import quopri
import pandas as pd


def decode_adr(vcf_data_list, i):
    # _______________decodiert die Verschlüsstelten Adress Daten aus dem vcf File
    # print('dekodiere adresse')
    if (
            vcf_data_list[i + 1][0] == "="
    ):  # prüft ob die Codierte message über mehrere Zeilen geht
        # geht die Codierte Adresse über mehrere Zeilen
        # werden diese in eine Variablen zusammengefasst um diese dann zu Decodieren
        print("mehrere zeilen")
        adress_data = vcf_data_list[i].split(":")[1] + vcf_data_list[i + 1][1:]
        adress = decode_qp(adress_data)
    else:
        adress = decode_qp(vcf_data_list[i].split(":")[1])
    # print(adress)
    return adress


def decode_qp(str_encoded):
    """
    Decodes the qp code and returns it as string
    :param str_encoded: The encoded qp string
    :return:
    """
    decoded = quopri.decodestring(str_encoded)
    decoded = decoded.decode("utf-8")
    decoded = decoded.split(";")[2]
    return decoded


# ________________________________________liest die Kontaktdatei vom Handy aus______________________
def vcf_read(csv_file,vcf_file):
    data = {
        "Name": [None],
        "Tel": [None],
        "Street": [None],
        "Hausnummer": [None],
        "Ort": [None],
        "Plz": [None],
    }
    dfKontakte = pd.read_csv(csv_file)
    # print(dfKontakte)
    with open(vcf_file, mode="r") as vcf:  # öffnet die vcf datei mit den Kontakte
        vcf_data = vcf.read()  # liest vcf file aus
        vcf_data_list = vcf_data.splitlines()  # trennt ausgelesenden file nach zeilen
        i = 0
        adresse = []
        while i + 1 < len(vcf_data_list):  # durchläuft einmal ganze liste
            name = "s"
            # tel='s'
            try:

                if (
                        vcf_data_list[i][0] + (vcf_data_list[i][1]) + (vcf_data_list[i][2])
                ) == "ADR":  # sucht Positionen die mit ADR beginnen in Liste (Zeichen für Adresse)
                    if "QUOTED-PRINTABLE" in vcf_data_list[i]:
                        # print(i)
                        adresse.append(decode_adr(vcf_data_list, i))
                    # Kontakt_new.append(tempkontakt)
                    else:
                        adresse.append(vcf_data_list[i].split(";")[3])
                    # print(i)
                    # print(len(adresse))
                    if len(adresse) == 2:

                        x = i
                        while not vcf_data_list[x][:3] in "TEL":
                            x = x - 1
                        tel = vcf_data_list[x].split(":")[1]
                        name = vcf_data_list[x - 1].split(":")[1]
                        ort = adresse[1].split(" ")
                        straße_l = adresse[0].split(" ")
                        street_name = ""
                        Ort_name = ""
                        for t in ort:
                            if t.isdigit():
                                plz = t
                            else:
                                Ort_name = Ort_name + " " + t
                        for t in straße_l:
                            if t.isdigit():
                                hausnummer_i = t
                            else:
                                street_name = street_name + " " + t
                        data = {
                            "Name": [name],
                            "Tel": [tel],
                            "Street": [street_name],
                            "Hausnummer": [hausnummer_i],
                            "Ort": [Ort_name],
                            "Plz": [plz],
                        }
                        # print(file_path)
                        new = test_contact_exists(name, dfKontakte)
                        if new:
                            print("neuer Kontakt gefunden")
                            df2 = pd.DataFrame(data)
                            #   print(df2)
                            dfKontakte = dfKontakte.append(df2)
                        # print(dfKontakte)
                        adresse = []
            except Exception as e:
                print(e)
                # print(file_path)
                # print('df2')
            i = i + 1
    dfKontakte.to_csv(csv_file, index=False)

    x = 0


def test_contact_exists(name, df_Kontakte):
    """
    Checks if a new contact is already in list
    :param name:    The file_path of the contact
    :param df_Kontakte: Dataframe with all contacts
    :return:    True if exists
    """
    # kontrolliert ob der neue Kontakt bereits vorhanden ist und
    # gibt dementsprechend True oder False zurück
    contact_exists = False
    for i, row in df_Kontakte.iterrows():
        # print(row)
        if row.get("Name") == name:
            print("der Kontakt ist bereits vorhanden")
            contact_exists = True
            break

    return contact_exists