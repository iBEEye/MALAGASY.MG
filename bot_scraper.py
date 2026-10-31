"""
MALAGASY.MG - Bot Mpanangona sy Mpanara-maso Vaovao
Mandeha ho azy amin'ny GitHub Actions maimaim-poana.
Mikaroka vaovao vaovao avy amin'ny MaLiNa, SIOKA, ary CENI.
"""

import urllib.request
import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime

# 1. Lisitry ny teny fototra harahi-maso (Anaran'ireo mpanao politika)
TENY_HOKAROHINA = [
    "Rajoelina", "Ravalomanana", "Rajaonarimampianina", "Ratsiraka",
    "Zafy", "Tsiranana", "Ramanantsoa", "Ratsimandrava", "Siteny",
    "Gascar", "Dadafara", "Dama", "Vahombey", "Mailhol", "Razanamasy",
    "Andriamanjato", "Naina Andriantsitohaina", "Tahina Razafinjoelina"
]

# 2. Loharano arahi-maso (Flux RSS sy Rohy mpanamarina vaovao)
LOHARANO_RSS = [
    {
        "anarana": "MaLiNa (Mpanao Gazety Mpanadihady)",
        "url": "https://malina.mg/feed/",
        "loharano_type": "rss"
    },
    {
        "anarana": "CENI Madagasikara (Vaovao Ofisialy)",
        "url": "https://ceni-madagascar.mg/feed/",
        "loharano_type": "rss"
    }
]

def manadio_soratra(soratra):
    """Manala ireo balises HTML amin'ny lahatsoratra"""
    if not soratra:
        return ""
    madio = re.sub(r'<[^>]+>', '', soratra)
    return madio.strip()

def mikaroka_vaovao():
    print("=" * 60)
    print(f"🚀 Fiantombohan'ny fisavana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    vaovao_voaangona = []

    for loharano in LOHARANO_RSS:
        print(f"📡 Eo am-pamahana ny: {loharano['anarana']}...")
        try:
            req = urllib.request.Request(
                loharano["url"],
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) MALAGASY.MG Bot/1.0'}
            )
            with urllib.request.urlopen(req, timeout=15) as valiny:
                xml_data = valiny.read()
                root = ET.fromstring(xml_data)

                # Famakiana ireo singa rehetra anaty RSS (<item>)
                for item in root.findall('.//item'):
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    date_elem = item.find('pubDate')
                    desc_elem = item.find('description')

                    lohateny = title_elem.text if title_elem is not None else ""
                    rohy = link_elem.text if link_elem is not None else ""
                    daty = date_elem.text if date_elem is not None else ""
                    famintinana = manadio_soratra(desc_elem.text) if desc_elem is not None else ""

                    # Fanamarinana raha misy anarana mpanao politika voatonona
                    lahatsoratra_feno = f"{lohateny} {famintinana}".lower()
                    
                    olona_voatonona = [
                        anarana for anarana in TENY_HOKAROHINA 
                        if anarana.lower() in lahatsoratra_feno
                    ]

                    if olona_voatonona:
                        vaovao_voaangona.append({
                            "lohateny": lohateny,
                            "rohy": rohy,
                            "daty": daty,
                            "famintinana": famintinana[:200] + "..." if len(famintinana) > 200 else famintinana,
                            "mpanamarina": loharano["anarana"],
                            "olona_voakasika": olona_voatonona,
                            "daty_nahitana": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        print(f"   🎯 Vaovao hita momba an'i: {', '.join(olona_voatonona)}")

        except Exception as e:
            print(f"   ⚠️ Tsy afaka nidirana ny {loharano['anarana']}: {e}")

    # 3. Fitehirizana ny valiny anaty rakitra JSON
    rakitra_fivoahana = "vaovao_vao_hita.json"
    with open(rakitra_fivoahana, "w", encoding="utf-8") as f:
        json.dump(vaovao_voaangona, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print(f"✅ Vita ny asa: Vaovao {len(vaovao_voaangona)} no voarakitra ao amin'ny '{rakitra_fivoahana}'.")
    print("=" * 60)

if __name__ == "__main__":
    mikaroka_vaovao()