import random

# Failide nimed
KÜSIMUSED_FAIL = "kusimused_vastused.txt"
VASTUVÕETUD_FAIL = "vastuvõetud.txt"
EISOBI_FAIL = "eisoobi.txt"
KÕIK_FAIL = "koik.txt"
STATISTIKA_FAIL = "statistika.txt"

# Andmestruktuurid
testitud_kandidaadid = {}
sobivad = []
mittesobivad = []

def loo_email(nimi):
    eesnimi, perenimi = nimi.lower().split()
    return f"{eesnimi}.{perenimi}@gmail.com"

def lae_küsimused():
    küsimused = []
    with open(KÜSIMUSED_FAIL, "r", encoding="utf-8") as f:
        for rida in f:
            if ':' in rida:
                k, v = rida.strip().split(":", 1)
                küsimused.append((k.strip(), v.strip().lower()))
    return küsimused

def testi_kandidaat(nimi, küsimused):
    valitud = random.sample(küsimused, 5)
    punktid = 0
    print(f"\nTest algas: {nimi}")
    for i, (küsimus, õige_vastus) in enumerate(valitud, 1):
        vastus = input(f"{nimi}, küsimus {i}: {küsimus} ").strip().lower()
        if vastus == õige_vastus:
            punktid += 1
    return punktid

def logi_tulemus(nimi, punktid):
    sobivus = "SOBIB" if punktid >= 3 else "EI SOBI"
    with open("tulemus_logi.txt", "a", encoding="utf-8") as f:
        f.write(f"{nimi} - {punktid} punkti - {sobivus}\n")

def salvesta_tulemused():
    with open(VASTUVÕETUD_FAIL, "w", encoding="utf-8") as f:
        for nimi, punktid in sorted(sobivad, key=lambda x: -x[1]):
            f.write(f"{nimi} - {punktid} punkti\n")

    with open(EISOBI_FAIL, "w", encoding="utf-8") as f:
        for nimi, punktid in sorted(mittesobivad):
            f.write(f"{nimi} - {punktid} punkti\n")

    with open(KÕIK_FAIL, "w", encoding="utf-8") as f:
        for nimi, (punktid, email) in testitud_kandidaadid.items():
            f.write(f"{nimi}, {punktid}, {email}\n")

    parim = max(testitud_kandidaadid.items(), key=lambda x: x[1][0])
    with open(STATISTIKA_FAIL, "w", encoding="utf-8") as f:
        f.write(f"Kokku kandidaate: {len(testitud_kandidaadid)}\n")
        f.write(f"Edukalt läbinud: {len(sobivad)}\n")
        f.write(f"Ei sobinud: {len(mittesobivad)}\n")
        f.write(f"Parim kandidaat: {parim[0]} ({parim[1][0]} punkti)\n")

def saada_epostid():
    for nimi, (punktid, email) in testitud_kandidaadid.items():
        print(f"Saadetud {email}: Tere {nimi}, sinu tulemuseks jäi {punktid} punkti.")

def saada_aruanne_tooleandjale():
    print("\nSaadetud tööandjale: tootaja@firma.ee\n")
    print("Tänase testimise tulemused:\n")
    for nimi, (punktid, email) in testitud_kandidaadid.items():
        sobivus = "SOBIB" if punktid >= 3 else "EI SOBI"
        print(f"{nimi} - {punktid} punkti - {email} - {sobivus}")
    parim = max(testitud_kandidaadid.items(), key=lambda x: x[1][0])
    print(f"\nParim kandidaat: {parim[0]} ({parim[1][0]} punkti)")
    print("Tervitustega, Testimissüsteem\n")

def main():
    küsimused = lae_küsimused()
    while len(sobivad) < 5:
        nimi = input("\nSisesta kandidaadi nimi (eesnimi perenimi): ").strip().title()
        if nimi in testitud_kandidaadid:
            print("See kandidaat on juba testitud.")
            continue
        punktid = testi_kandidaat(nimi, küsimused)
        email = loo_email(nimi)
        testitud_kandidaadid[nimi] = (punktid, email)
        logi_tulemus(nimi, punktid)
        if punktid >= 3:
            sobivad.append((nimi, punktid))
            print(f"{nimi} sobib. Tulemuseks {punktid} punkti.")
        else:
            mittesobivad.append((nimi, punktid))
            print(f"{nimi} ei sobi. Tulemuseks {punktid} punkti.")

    salvesta_tulemused()
    saada_epostid()
    saada_aruanne_tooleandjale()

    print("\nSobivad kandidaadid:")
    for nimi, punktid in sorted(sobivad, key=lambda x: -x[1]):
        print(f"{nimi} - {punktid} punkti")

    print("\nMittesobivad kandidaadid:")
    for nimi, _ in sorted(mittesobivad):
        print(nimi)

    print("\nTulemused saadeti e-posti aadressidele.")