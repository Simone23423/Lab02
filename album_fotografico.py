import csv
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        album = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            # Salta la prima riga contenente le intestazioni
            next(reader, None)
            for riga in reader:
                if not riga or len(riga) < 5:
                    continue  # Salta eventuali righe vuote
                codice = riga[0].strip()
                titolo = riga[1].strip()
                autore = riga[2].strip()
                mese = int(riga[3].strip())
                anno = int(riga[4].strip())
                # Cerca se l'anno è già presente nell'album
                blocco_anno = None
                for elemento in album:
                    if elemento["anno"] == anno:
                        blocco_anno = elemento
                        break
                # Se l'anno non è ancora presente, lo crea e lo aggiunge alla struttura
                if blocco_anno is None:
                    blocco_anno = {"anno": anno, "foto": []}
                    album.append(blocco_anno)
                # Aggiunge i dati della foto alla lista dell'anno corrispondente
                blocco_anno["foto"].append(
                    {
                        "codice": codice,
                        "titolo": titolo,
                        "autore": autore,
                        "mese": mese,
                    }
                )
        return album
    except FileNotFoundError:
        return None
def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # 1. Controllo validità mese (deve essere compreso tra 1 e 12)
    if mese < 1 or mese > 12:
        return None
    if cerca_foto(album, codice) is not None:
        return None
    blocco_anno = None
    for elemento in album:
        if elemento["anno"] == anno:
            blocco_anno = elemento
            break
    if blocco_anno is None:
        blocco_anno = {"anno": anno, "foto": []}
        album.append(blocco_anno)
    blocco_anno["foto"].append(
        {
            "codice": codice,
            "titolo": titolo,
            "autore": autore,
            "mese": mese,
        }
    )
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None
    return album
def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    if album is None:
        return None
    for blocco_anno in album:
        anno = blocco_anno["anno"]
        for foto in blocco_anno["foto"]:
            if foto["codice"] == codice:
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {anno}"
    return None
def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if album is None:
        return None
    for blocco_anno in album:
        if blocco_anno["anno"] == anno:
            titoli = [foto["titolo"] for foto in blocco_anno["foto"]]
            titoli.sort()
            return titoli

    return None

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()