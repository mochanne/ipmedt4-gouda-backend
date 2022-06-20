import re
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




def CheckCompleteness(path):
    total_tests = 0
    good_tests = 0
    NL = '\n     > '
    helps = set()
    print("Data completeness test voor",path)

    def good(*args):
        nonlocal total_tests
        nonlocal good_tests
        total_tests += 1
        good_tests += 1
        print('  ✅',*args)
    def bad(*args, help=None):
        nonlocal total_tests
        total_tests += 1
        print('  ❌',*args)
        if help != None:
            print('     🛈',help)
            helps.add('     🛈 '+help)
    def check(condition,prompt="klopt",suffix=" niet", ormode = False, help=None):
        if condition:
            good(prompt)
        else:
            if ormode:
                bad(suffix, help=help)
            else:
                bad(prompt+suffix, help=help)
        return condition
    contents = os.listdir(path)
    if check('waypoints.json' in contents, "waypoints.json bestaat", help="Gebruik de 'Waypoints invullen' actie van dit tool."):
        with open(path+'/waypoints.json','r') as f:
            try:
                in_ = json.loads(f.read())
                good('waypoints.json is valid json')
                check(len(in_) >= 2, f'waypoints.json heeft genoeg items ({len(in_)})', f'waypoints.json heeft niet genoeg items ({len(in_)})', True, "Gebruik de 'Waypoints invullen' actie van dit tool en voer minstens 2 coordinaten in.")
            except json.JSONDecodeError as e:
                bad('waypoints.json is invalid json!',e, help="Gebruik de 'Waypoints invullen' actie van dit tool en voer minstens 2 coordinaten in.")
    else:
        bad('waypoints.json is invalid json!', help="Gebruik de 'Waypoints invullen' actie van dit tool en voer minstens 2 coordinaten in.")

    dirs = GetDirs(path)
    check(len(dirs) > 2, f"Er zijn genoeg infopoints ({len(dirs)})", f"Er zijn niet genoeg infopoints ({len(dirs)})", True, help="Download het dataset opnieuwe met scraper.py")
    check(any([item.startswith(str(i+1)) and '$' in item for i,item in enumerate(dirs)]), 'Infopoints zijn correct gesorteerd', f'Infopoints zijn niet correct gesorteerd: {NL}{NL.join(dirs)}', True, "Gebruik de 'Sorteer' actie van dit tool.")
    
    missing_images = []
    missing_json = []
    missing_lat_long = []
    scuffed_text = []
    for item in dirs:
        mypath = path+'/'+item
        found_img = False
        for subitem in os.listdir(mypath):            
            if subitem.startswith('img.'):
                found_img = True
        if not found_img:
            missing_images.append(item)
        if 'data.json' in os.listdir(mypath):
            with open(mypath+'/data.json', 'r') as f:
                in_ = json.loads(f.read())
                if len(IdentifyHtmlScuff(in_['gedicht'])) > 0 or len(IdentifyHtmlScuff(in_['info'])) > 0:
                    scuffed_text.append(item+'/data.json')
                if in_.get('latitude') == None or in_.get('longitude') == None:
                    missing_lat_long.append(item+'/data.json')

        else:
            missing_json.append(item)
            missing_lat_long.append(item+'/data.json')

    check(len(scuffed_text) == 0, 'Alle gedichten en info tekst bij de infopoints zijn correct geformateerd.', f'Infopoints hebben correct geformateerde gedichten/info tekst: {NL}{NL.join(scuffed_text)}', True, "Gebruik de 'Tekst formaat fixen' actie van dit tool.")
    check(len(missing_images) == 0, 'Alle infopoints hebben afbeeldingen', f'Deze {len(missing_images)} infopoints missen een afbeelding: {NL}{NL.join(missing_images)}', True, 'Download het dataset opnieuw met scraper.py')
    check(len(missing_json) == 0, 'Alle infopoints hebben data', f'Deze {len(missing_json)} infopoints missen data: {NL}{NL.join(missing_json)}', True, 'Download het dataset opnieuw met scraper.py')
    check(len(missing_lat_long) == 0, 'Alle infopoints hebben een latitude & longitude waarde', f'Deze {len(missing_lat_long)} infopoints missen een latitude en/of longitude waarde: {NL}{NL.join(missing_lat_long)}', True, "Gebruik de 'Infopoints invullen' actie van dit tool.")

    print()
    if not check(total_tests == good_tests, f"{good_tests}/{total_tests} testen correct: Data is OK", f"{good_tests}/{total_tests} testen correct: Data heeft ingrijp nodig", True):
        print("    Aangeraden acties:")
        print('\n'.join(helps))
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
    items = GetDirs(path)
    print("copy-paste coordinaten van google maps & druk enter")
    print("vul STOP in om te stoppen")
    print("vul niks in om het huidige item over te slaan")
    for i,item in enumerate(items):
        print(f"   {i+1}/{len(items)}: "+item)
        choice = input('>')
        if choice == "":
            continue
        elif choice.lower() == "stop":
            break
        else:
            try:
                lat, long = [float(a.strip()) for a in choice.split(',')]
                with open(path+'/'+item+'/data.json', 'r') as f:
                    in_ = f.read()
                    jsono = json.loads(in_)

                with open(path+'/'+item+'/data.json', 'w') as f:
                    jsono['longitude'] = long
                    jsono['latitude'] = lat
                    f.write(json.dumps(jsono))
            except Exception as e:
                print('Ongeledige input:',e)
                raise e
        print()

def IdentifyHtmlScuff(text:str):
    items = []

    for i in re.finditer('[^\n^ ^\.][A-Z][a-z]+', text):
        items.insert(0,i.start(0))
    return items

def HtmlDeScuffer(text, indexes):
    out = text
    for i in indexes:
        out = out[:i+1]+". "+out[i+1:]
    return out

def InteractiveTextFixer(path):
    anychanged = False
    for p in GetDirs(path):
        with open(path+'/'+p+'/data.json','r') as f:
            data = json.loads(f.read())
        changed = False
        for key in ['gedicht', 'info']:
            if len(x:=IdentifyHtmlScuff(data[key])) > 0:
                data[key] = HtmlDeScuffer(data[key], x)
                changed = True
                anychanged = True
                print(p+':',key,'gefixed')

        if changed:
            with open(path+'/'+p+'/data.json','w') as f:
                f.write(json.dumps(data))
    if not anychanged:
        print("Tekst was al OK; geen veranderingen gemaakt")
    print("klaar")

def InteractiveWaypointEnter(path):
    out = []
    print("copy-paste coordinaten van google maps & druk enter")
    print("vul STOP in om te stoppen")
    while True:
        choice = input('>')
        if choice.lower() == "stop":
            break
        else:
            try:
                lat, long = [float(aangemaakt.strip()) for a in choice.split(', ')]
                out.append({'longitude': long, 'latitude': lat})
            except Exception as e:
                print('Ongeledige input:',e)
    with open(path+'/waypoints.json', 'w') as f:
        print('Waypoints:', out)
        f.write(json.dumps(out))
        print('Opgeslagen als '+path+'/waypoints.json')

acties = {'Sorteer': InteractiveDirectorySort, 'Infopoints invullen': InteractiveInfoPointAdder, 'Verifieer data completeness':CheckCompleteness, 'Waypoints invullen':InteractiveWaypointEnter, 'Tekst formaat fixen':InteractiveTextFixer, 'Sluit programma':exit}

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