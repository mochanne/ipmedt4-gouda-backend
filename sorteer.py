import os
import json

def choose(choices:list, prompt:str="Kies een optie:", vraag="Nummer: ", return_index=False):
    print(prompt)
    ran = len(choices)
    while True:
        print('\n'.join([f"   [{i}] {a}" for i,a in enumerate(choices)]))
        print()
        keuze = input(vraag)
        try:
            if return_index:
                if int(keuze) in range(ran):
                    return int(keuze)
            else:
                return choices[int(keuze)]
        except Exception as e:
                print(e)
        print("Ongeldige keuze.")
        print()

def dirsort(a):
    return int(a.split('$')[0]) if '$' in a else 9999

def GetDirs(path):
    items = [a for a in os.listdir(path) if os.path.isdir(path+'/'+a)]
    items.sort(key=dirsort)
    return items

def InteractiveDirectorySort(path):
    items = GetDirs(path)
    items.sort(key=dirsort)
    out = []

    for i in range(len(items)):
        get = choose(items, f"Welk punt komt op positie {i+1}?")
        items.remove(get)
        out.append(get)
        line()

    print('Klopt dit?')
    print('\n'.join((["   "+a for a in out])))
    if input('\n[y/N]').lower() != 'y':
        print("Geannuleerd")
        return
    for i,item in enumerate(out):
        newname = f'{i+1}$'+item.split('$')[-1]
        os.rename(path+'/'+item, path+'/'+newname)

def InteractiveInfoPointAdder(path):
    pass

def InteractiveWaypointEnter(path):
    pass

acties = {'Sorteer': InteractiveDirectorySort, 'Infopoints invullen': None, 'Waypoints invullen':None}

def line():
    print('-'*30)

def main():
    keuzes = os.listdir('wandelroutes')

    path = f'wandelroutes/{choose(keuzes, "Kies een route:")}'
    line()
    
    actie = acties[choose(list(acties.keys()), "Kies een actie:")]
    line()
    
    actie(path)


if __name__ == "__main__":
    main()