import random
import smtplib
import ssl
from email.message import EmailMessage
from tkinter import filedialog
import tkinter as tk

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
    osad = nimi.lower().split()
    if len(osad) >= 2:
        eesnimi = osad[0]
        perenimi = osad[1]
    elif len(osad) == 1:
        eesnimi = osad[0]
        perenimi = "kandidaat"
    else:
        eesnimi = "nimi"
        perenimi = "puudub"
    
    return f"{eesnimi}{perenimi}@gmail.com"


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
def new_quest(quest: str):
    print("\n=== Lisa uus küsimus ===")
    küsimus = input("Sisesta küsimus: ").strip()
    vastus = input("Sisesta õige vastus: ").strip().lower()

    if küsimus and vastus:
        with open(KÜSIMUSED_FAIL, "a", encoding="utf-8") as f:
            f.write(f"{küsimus}:{vastus}\n")
        print("Küsimus lisatud!")
    else:
        print("Tühja küsimust või vastust ei saa lisada.")

def salvesta_tulemused():
    # Funktsioon, mis sorteerib kandidaate, ilma lambda kasutamata
    def sorteerige_sobivad(kandidaadid):
        tulemused = []
        for nimi, punktid in kandidaadid:
            tulemused.append((nimi, punktid))
        tulemused.sort(key=sorteeri_punktide_jargi, reverse=True)
        return tulemused

    def sorteerige_punktide_jargi(kandidaat):
        return kandidaat[1]
    
    sobivad_sorted = sorteerige_sobivad(sobivad)
    mittesobivad_sorted = sorteerige_sobivad(mittesobivad)

    with open(VASTUVÕETUD_FAIL, "w", encoding="utf-8") as f:
        for nimi, punktid in sobivad_sorted:
            f.write(f"{nimi} - {punktid} punkti\n")

    with open(EISOBI_FAIL, "w", encoding="utf-8") as f:
        for nimi, punktid in mittesobivad_sorted:
            f.write(f"{nimi} - {punktid} punkti\n")

    with open(KÕIK_FAIL, "w", encoding="utf-8") as f:
        for nimi, (punktid, email) in testitud_kandidaadid.items():
            f.write(f"{nimi}, {punktid}, {email}\n")

    parim = max(testitud_kandidaadid.items(), key=parima_kandidaadi_valik)
    with open(STATISTIKA_FAIL, "w", encoding="utf-8") as f:
        f.write(f"Kokku kandidaate: {len(testitud_kandidaadid)}\n")
        f.write(f"Edukalt läbinud: {len(sobivad)}\n")
        f.write(f"Ei sobinud: {len(mittesobivad)}\n")
        f.write(f"Parim kandidaat: {parim[0]} ({parim[1][0]} punkti)\n")

def parima_kandidaadi_valik(kandidaat):
    return kandidaat[1][0]

def saada_epostid():
    for nimi, (punktid, email) in testitud_kandidaadid.items():
        print(f"Saadetud {email}: Tere {nimi}, sinu tulemuseks jäi {punktid} punkti.")
def sortimisalus_punktide_jargi(kandidaat):
    return kandidaat[1]
def main():
    küsimused = lae_küsimused()
    
    # Tkinter akna loomiseks
    root = tk.Tk()
    root.withdraw()  # Ei soovi kuvada täiendavat Tkinter akent

    def saada_tulemus_email(nimi, punktid, email):
        msg = EmailMessage()
        msg['Subject'] = 'Sinu testitulemus'
        msg['From'] = 'eha20082@gmail.com'
        msg['To'] = email

        text_sisu = f"Tere, {nimi}! Sinu tulemuseks jäi {punktid} punkti."

        if punktid >= 3:
            html_sisu = f"""\
            <html>
            <body>
                <h1>Tere, {nimi}!</h1>
                <p>Sa sooritasid testi edukalt – {punktid} punkti!</p>
                <p>Jätka samas vaimus!</p>
            </body>
            </html>
            """
        else:
            html_sisu = f"""\
            <html>
            <body>
                <h1>Tere, {nimi}!</h1>
                <p>Kahjuks said sa ainult {punktid} punkti.</p>
                <p>Ära heida meelt – harjutamine teeb meistriks!</p>
            </body>
            </html>
            """

        msg.set_content(text_sisu)
        msg.add_alternative(html_sisu, subtype='html')

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls(context=ssl.create_default_context())
                server.login('eha20082@gmail.com', 'pjuj tvvc ogta dxkb')
                server.send_message(msg)
            print(f"E-kiri saadetud: {email}")
        except Exception as e:
            print(f"Viga e-kirja saatmisel: {e}")

    while True:
        print("\n---- MENÜÜ ----")
        print("1. Testi uut kandidaati")
        print("2. Näita parimaid kandidaate")
        print("3. Lisa uus küsimus")
        print("4. Välju")
        valik = input("Vali tegevus (1-4): ").strip()
        if valik == "1":
            if len(sobivad) >= 5:
                print("Piisavalt sobivaid kandidaate testitud.")
                continue

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

            saada_tulemus_email(nimi, punktid, email)

        elif valik == "2":
            print("\n=== PARIMAD KANDIDAADID ===")
            parimad = sorted(sobivad, key=sortimisalus_punktide_jargi, reverse=True)[:3]
            for i, (nimi, punktid) in enumerate(parimad, 1):
                print(f"{i}. {nimi} - {punktid} punkti")

        elif valik == "3":
            lisa_küsimus()

        elif valik == "4":
            salvesta_tulemused()
            print("Andmed salvestatud. Head aega!")
            break
        else:
            print("Tundmatu valik, proovi uuesti.")