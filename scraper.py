from playwright.sync_api import sync_playwright
import json
from datetime import datetime
from urllib.parse import urljoin

SITI = [
    {
        "nome": "ARIA",
        "url": "https://www.ariaspa.it/wps/portal/Aria/Home/bandi-convenzioni/bandi-di-gara/avvisi-sui-bandi",
    },
    {
        "nome": "Lombardia",
        "url": "https://www.bandi.regione.lombardia.it/servizi/servizio/bandi",
    },
    {
        "nome": "Milano",
        "url": "https://www2.comune.milano.it/comune/amministrazione-trasparente/bandi-di-gara-e-contratti",
    },
    {
        "nome": "Municipio2",
        "url": "https://www2.comune.milano.it/web/municipio-2/bandi",
    },
]

MIN_LUNGHEZZA_TESTO = 25  # scarta link troppo corti (es. "Home", "Contatti")


def estrai_bandi(page, sito):
    bandi = []
    links = page.query_selector_all("a")
    for link in links:
        try:
            testo = (link.inner_text() or "").strip()
            href = link.get_attribute("href")
            if not testo or not href or len(testo) < MIN_LUNGHEZZA_TESTO:
                continue
            url_completo = urljoin(sito["url"], href)
            bandi.append({
                "titolo": testo,
                "link": url_completo,
                "ente": sito["nome"],
                "data": "",
                "sito": sito["nome"],
                "estratto": datetime.now().isoformat()
            })
        except Exception:
            continue
    return bandi


def main():
    tutti_bandi = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(user_agent="Mozilla/5.0")

        for sito in SITI:
            print(f"Scraping {sito['nome']}...")
            try:
                page.goto(sito["url"], timeout=30000, wait_until="networkidle")
                page.wait_for_timeout(2000)  # extra attesa per contenuti lenti
                bandi = estrai_bandi(page, sito)
                print(f"  -> {len(bandi)} link trovati")
                tutti_bandi.extend(bandi)
            except Exception as e:
                print(f"  Errore su {sito['nome']}: {e}")

        browser.close()

    with open("bandi.json", "w", encoding="utf-8") as f:
        json.dump(tutti_bandi, f, indent=2, ensure_ascii=False)

    print(f"Salvati {len(tutti_bandi)} elementi totali in bandi.json")


if __name__ == "__main__":
    main()