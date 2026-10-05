import os

def leggi_studenti(nome_file):
    """
    Legge il file CSV degli studenti e restituisce una lista di dizionari.
    Ignora l'intestazione e converte subito ID in intero e media in float.
    """
    studenti = []
    
    with open(nome_file, 'r', encoding='utf-8') as f:
        #Salta la prima riga di intestazione (ID,cognome,nome,classe,media)
        next(f)
        
        for riga in f:
            #Rimuove eventuali spazi bianchi e il carattere di "a capo" (\n)
            riga = riga.strip()
            if not riga:
                continue
            
            #Separa i campi usando la virgola
            parti = riga.split(',')
            
            #Salva i dati in un dizionario convertendo i tipi numerici
            studente = {
                'id': int(parti[0]),
                'cognome': parti[1],
                'nome': parti[2],
                'classe': parti[3],
                'media': float(parti[4])
            }
            studenti.append(studente)
            
    return studenti


def leggi_richieste(nome_file):
    """
    Legge il file delle richieste e ricava:
    - la lista degli ID da cercare (convertiti in interi)
    - il cognome da cercare
    - la classe di cui calcolare la media
    """
    with open(nome_file, 'r', encoding='utf-8') as f:
        # Raccoglie tutte le righe non vuote rimuovendo gli "a capo"
        righe = [riga.strip() for riga in f if riga.strip()]
    
    #Riga 1: elenchi di ID separati da virgola -> conversione in int
    lista_id = [int(id_str) for id_str in righe[0].split(',')]
    
    #Riga 2: cognome da cercare
    cognome = righe[1]
    
    #Riga 3: classe da analizzare
    classe = righe[2]
    
    return lista_id, cognome, classe


def cerca_per_id(studenti, id_cercato):
    """
    Cerca uno studente per ID.
    Restituisce il dizionario dello studente se trovato, altrimenti None.
    """
    for studente in studenti:
        if studente['id'] == id_cercato:
            return studente
    return None


def stampa_studente(studente):
    """
    Stampa i dati dello studente separati da uno spazio:
    ID cognome nome classe media
    """
    print(f"{studente['id']} {studente['cognome']} {studente['nome']} {studente['classe']} {studente['media']}")


# --- PROGRAMMA PRINCIPALE ---
def main():
    #1. Trova il percorso assoluto della cartella in cui si trova questo file .py
    cartella_script = os.path.dirname(os.path.abspath(__file__))

    #2. Unisce la cartella dello script con i nomi dei file di testo
    percorso_studenti = os.path.join(cartella_script, 'studenti.csv')
    percorso_richieste = os.path.join(cartella_script, 'richieste.txt')

    #3. Lettura dei file usando i percorsi sicuri
    studenti = leggi_studenti(percorso_studenti)
    lista_id, cognome_cercato, classe_cercata = leggi_richieste(
        percorso_richieste
    )

    #4. Prima richiesta: Ricerca per ID
    print('--- Ricerca per ID ---')
    for id_cercato in lista_id:
        studente = cerca_per_id(studenti, id_cercato)
        if studente:
            stampa_studente(studente)
        else:
            print(f'ID {id_cercato} non trovato')

    #5. Seconda richiesta: Ricerca per Cognome (insensibile alle maiuscole)
    print(f'Ricerca per cognome: {cognome_cercato}')
    trovati = False
    for studente in studenti:
        #Converte in minuscolo con .lower() per confrontare senza distinguere maiuscole/minuscole
        if studente['cognome'].lower() == cognome_cercato.lower():
            stampa_studente(studente)
            trovati = True

    if not trovati:
        print('Nessuno studente trovato')

    #6. Terza richiesta: Calcolo della media della classe
    print(f'Media della classe {classe_cercata}')
    somma_medie = 0.0
    conteggio = 0

    for studente in studenti:
        if studente['classe'].upper() == classe_cercata.upper():
            somma_medie += studente['media']
            conteggio += 1

    if conteggio > 0:
        media_generale = somma_medie / conteggio
        print(f'Studenti considerati: {conteggio}')
        print(f'Media: {media_generale:.2f}')  #Arrotonda a due cifre decimali
    else:
        print(f'Nessuno studente nella classe {classe_cercata}')


if __name__ == '__main__':
    main()