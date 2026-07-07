import json
import os

DOSYA_ADI = "turnuva_verisi.json"


def turnuva_olustur():
    son_16 = [
        {"tur": "Son 16", "takim1": "Kanada", "takim2": "Fas", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
        {"tur": "Son 16", "takim1": "Paraguay", "takim2": "Fransa", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
        {"tur": "Son 16", "takim1": "Portekiz", "takim2": "İspanya", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
        {"tur": "Son 16", "takim1": "ABD", "takim2": "Belçika", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
        {"tur": "Son 16", "takim1": "Brezilya", "takim2": "Norveç", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
        {"tur": "Son 16", "takim1": "Meksika", "takim2": "İngiltere", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
        {"tur": "Son 16", "takim1": "Arjantin", "takim2": "Mısır", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
        {"tur": "Son 16", "takim1": "İsviçre", "takim2": "Kolombiya", "skor1": None, "skor2": None, "oynandi": False, "kazanan": None},
    ]
    return son_16


def mac_bul(maclar, takim_adi):
    for mac in maclar:
        if takim_adi.lower() in [mac["takim1"].lower(), mac["takim2"].lower()]:
            return mac
    return None


def veriyi_kaydet(turnuva, aktif_tur, istatistikler):
    veri = {
        "turnuva": turnuva,
        "aktif_tur": aktif_tur,
        "istatistikler": istatistikler
    }
    with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, ensure_ascii=False, indent=2)
    print("Veriler başarıyla kaydedildi!")


def veriyi_yukle():
    if not os.path.exists(DOSYA_ADI):
        return None

    with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
        veri = json.load(dosya)
    return veri


def oyuncu_istatistigi_guncelle(istatistikler, oyuncu_adi, takim, gol=0, asist=0):
    for oyuncu in istatistikler:
        if oyuncu["oyuncu"].lower() == oyuncu_adi.lower():
            oyuncu["gol"] += gol
            oyuncu["asist"] += asist
            return
    istatistikler.append({"oyuncu": oyuncu_adi, "takim": takim, "gol": gol, "asist": asist})


def gol_detaylarini_gir(mac, istatistikler):
    toplam_gol = mac["skor1"] + mac["skor2"]
    if toplam_gol == 0:
        return

    print(f"\nBu maçta toplam {toplam_gol} gol atıldı. Şimdi golleri tek tek girelim.")
    for i in range(toplam_gol):
        print(f"\n{i + 1}. gol:")
        takim = input(f"Hangi takım attı? ({mac['takim1']} / {mac['takim2']}): ")

        if takim.lower() == mac["takim1"].lower():
            takim_adi = mac["takim1"]
        elif takim.lower() == mac["takim2"].lower():
            takim_adi = mac["takim2"]
        else:
            print("Geçersiz takım adı, bu gol atlanıyor.")
            continue

        oyuncu = input("Golü atan oyuncu: ")
        asist = input("Asist yapan oyuncu (yoksa boş bırakıp Enter'a basın): ")

        oyuncu_istatistigi_guncelle(istatistikler, oyuncu, takim_adi, gol=1)
        if asist.strip():
            oyuncu_istatistigi_guncelle(istatistikler, asist, takim_adi, asist=1)


def mac_sonucu_gir(maclar, istatistikler):
    print("\nBu turdaki takımlar:")
    for mac in maclar:
        durum = "✓ Oynandı" if mac["oynandi"] else "Bekliyor"
        print(f"  {mac['takim1']} - {mac['takim2']} ({durum})")

    takim_adi = input("\nSonucunu gireceğiniz maçtaki bir takımı yazın: ")
    mac = mac_bul(maclar, takim_adi)

    if not mac:
        print("Hata: Bu isimde takım bulunamadı!")
        return

    if mac["oynandi"]:
        print("Bu maç zaten kaydedilmiş!")
        return

    try:
        skor1 = int(input(f"{mac['takim1']} attığı gol: "))
        skor2 = int(input(f"{mac['takim2']} attığı gol: "))
    except ValueError:
        print("Hata: Gol sayısı tam sayı olmalı!")
        return

    if skor1 == skor2:
        print("Uyarı: Eleme turunda beraberlik olmaz! Uzatma/penaltı sonucuna göre kazananı belirtin.")
        kazanan_adi = input("Uzatmalar/penaltılar sonrası kazanan: ")
        if kazanan_adi.lower() == mac["takim1"].lower():
            mac["kazanan"] = mac["takim1"]
        elif kazanan_adi.lower() == mac["takim2"].lower():
            mac["kazanan"] = mac["takim2"]
        else:
            print("Hata: Geçersiz takım adı!")
            return
    else:
        mac["kazanan"] = mac["takim1"] if skor1 > skor2 else mac["takim2"]

    mac["skor1"] = skor1
    mac["skor2"] = skor2
    mac["oynandi"] = True
    print(f"Kaydedildi! Kazanan: {mac['kazanan']}")

    gol_detaylarini_gir(mac, istatistikler)


def tur_goster(maclar, tur_adi):
    print(f"\n--- {tur_adi.upper()} ---")
    for mac in maclar:
        if mac["oynandi"]:
            print(f"  {mac['takim1']} {mac['skor1']} - {mac['skor2']} {mac['takim2']}  ➜ Kazanan: {mac['kazanan']}")
        else:
            print(f"  {mac['takim1']} vs {mac['takim2']}  (henüz oynanmadı)")


def sonraki_tur_adi(mevcut_tur):
    siralama = ["Son 16", "Çeyrek Final", "Yarı Final", "Final"]
    index = siralama.index(mevcut_tur)
    if index + 1 < len(siralama):
        return siralama[index + 1]
    return None


def sonraki_tura_gec(turnuva, aktif_tur):
    mevcut_maclar = turnuva[aktif_tur]

    if not all(mac["oynandi"] for mac in mevcut_maclar):
        print("Hata: Bu turdaki tüm maçlar tamamlanmadan sonraki tura geçilemez!")
        return aktif_tur

    yeni_tur = sonraki_tur_adi(aktif_tur)
    if yeni_tur is None:
        sampiyon = mevcut_maclar[0]["kazanan"]
        print(f"\n🏆 TURNUVA ŞAMPİYONU: {sampiyon} 🏆")
        return aktif_tur

    kazananlar = [mac["kazanan"] for mac in mevcut_maclar]

    yeni_maclar = []
    for i in range(0, len(kazananlar), 2):
        yeni_maclar.append({
            "tur": yeni_tur,
            "takim1": kazananlar[i],
            "takim2": kazananlar[i + 1],
            "skor1": None, "skor2": None,
            "oynandi": False, "kazanan": None
        })

    turnuva[yeni_tur] = yeni_maclar
    print(f"\n{yeni_tur} turu oluşturuldu!")
    tur_goster(yeni_maclar, yeni_tur)
    return yeni_tur


def sampiyonluk_yolu_goster(turnuva):
    print("\n=== TURNUVA DURUMU ===")
    for tur_adi, maclar in turnuva.items():
        if maclar:
            tur_goster(maclar, tur_adi)


def gol_krallari_goster(istatistikler):
    if not istatistikler:
        print("Henüz gol/asist verisi girilmedi.")
        return

    siralanmis = sorted(istatistikler, key=lambda o: (o["gol"], o["asist"]), reverse=True)

    print("\n--- GOL KRALLIĞI TABLOSU ---")
    print("{:<20} {:<12} {:<5} {:<5}".format("Oyuncu", "Takım", "Gol", "Asist"))
    print("-" * 45)
    for o in siralanmis:
        print("{:<20} {:<12} {:<5} {:<5}".format(o["oyuncu"], o["takim"], o["gol"], o["asist"]))


def menu_goster():
    print("\n--- DÜNYA KUPASI 2026 ELEME TURU TAKİP SİSTEMİ ---")
    print("1. Maç Sonucu Gir")
    print("2. Turu Görüntüle")
    print("3. Sonraki Tura Geç")
    print("4. Şampiyonluk Yolunu Görüntüle")
    print("5. Gol Krallığı Tablosu")
    print("6. Çıkış")


def main():
    kayitli_veri = veriyi_yukle()

    if kayitli_veri:
        devam_et = input("Kayıtlı bir turnuva bulundu. Kaldığınız yerden devam etmek ister misiniz? (e/h): ")
        if devam_et.lower() == "e":
            turnuva = kayitli_veri["turnuva"]
            aktif_tur = kayitli_veri["aktif_tur"]
            istatistikler = kayitli_veri["istatistikler"]
            print("Kayıtlı veri yüklendi!")
        else:
            turnuva = {"Son 16": turnuva_olustur(), "Çeyrek Final": [], "Yarı Final": [], "Final": []}
            aktif_tur = "Son 16"
            istatistikler = []
    else:
        turnuva = {"Son 16": turnuva_olustur(), "Çeyrek Final": [], "Yarı Final": [], "Final": []}
        aktif_tur = "Son 16"
        istatistikler = []

    while True:
        menu_goster()
        secim = input("Seçiminiz: ")
        if secim == "6":
            print("Programdan çıkılıyor...")
            break
        elif secim == "1":
            mac_sonucu_gir(turnuva[aktif_tur], istatistikler)
            veriyi_kaydet(turnuva, aktif_tur, istatistikler)
        elif secim == "2":
            tur_goster(turnuva[aktif_tur], aktif_tur)
        elif secim == "3":
            aktif_tur = sonraki_tura_gec(turnuva, aktif_tur)
            veriyi_kaydet(turnuva, aktif_tur, istatistikler)
        elif secim == "4":
            sampiyonluk_yolu_goster(turnuva)
        elif secim == "5":
            gol_krallari_goster(istatistikler)
        else:
            print("Geçersiz seçim!")


if __name__ == "__main__":
    main()