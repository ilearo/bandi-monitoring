import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def scrape_aria():
    """Scrape bandi ARIA"""
    bandi = []
    url = "https://www.ariaspa.it/wps/portal/Aria/Home/bandi-convenzioni/bandi-di-gara/avvisi-sui-bandi"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Adatta i selettori al sito reale
        for item in soup.find_all('div', class_='bando-item')[:20]:  # Prendi i 20 più recenti
            try:
                titolo = item.find('a')
                if titolo:
                    bandi.append({
                        'titolo': titolo.get_text(strip=True),
                        'link': titolo.get('href', ''),
                        'ente': item.find('span', class_='ente').get_text(strip=True) if item.find('span', class_='ente') else '',
                        'data': item.find('span', class_='data').get_text(strip=True) if item.find('span', class_='data') else '',
                        'sito': 'ARIA',
                        'estratto': datetime.now().isoformat()
                    })
            except:
                continue
    except Exception as e:
        print(f"Errore ARIA: {e}")
    
    return bandi

def scrape_lombardia():
    """Scrape bandi Regione Lombardia"""
    bandi = []
    url = "https://www.bandi.regione.lombardia.it/"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Adatta i selettori
        for item in soup.find_all('div', class_='bando')[:20]:
            try:
                titolo = item.find('a')
                if titolo:
                    bandi.append({
                        'titolo': titolo.get_text(strip=True),
                        'link': titolo.get('href', ''),
                        'ente': 'Regione Lombardia',
                        'data': item.find('span', class_='data').get_text(strip=True) if item.find('span', class_='data') else '',
                        'sito': 'Lombardia',
                        'estratto': datetime.now().isoformat()
                    })
            except:
                continue
    except Exception as e:
        print(f"Errore Lombardia: {e}")
    
    return bandi

def scrape_milano():
    """Scrape bandi Comune di Milano"""
    bandi = []
    url = "https://www.comune.milano.it/siti/amministrazione-trasparente/bandi-di-gara"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        for item in soup.find_all('tr')[1:21]:  # Skip header
            try:
                cols = item.find_all('td')
                if len(cols) >= 2:
                    titolo = cols[0].find('a')
                    if titolo:
                        bandi.append({
                            'titolo': titolo.get_text(strip=True),
                            'link': titolo.get('href', ''),
                            'ente': 'Comune di Milano',
                            'data': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                            'sito': 'Milano',
                            'estratto': datetime.now().isoformat()
                        })
            except:
                continue
    except Exception as e:
        print(f"Errore Milano: {e}")
    
    return bandi

def scrape_municipio2():
    """Scrape bandi Municipio 2 Milano"""
    bandi = []
    url = "https://www.municipio2.milano.it/bandi"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'lxml')
        
        for item in soup.find_all('div', class_='bando-item')[:20]:
            try:
                titolo = item.find('a')
                if titolo:
                    bandi.append({
                        'titolo': titolo.get_text(strip=True),
                        'link': titolo.get('href', ''),
                        'ente': 'Municipio 2 Milano',
                        'data': item.find('span', class_='data').get_text(strip=True) if item.find('span', class_='data') else '',
                        'sito': 'Municipio2',
                        'estratto': datetime.now().isoformat()
                    })
            except:
                continue
    except Exception as e:
        print(f"Errore Municipio 2: {e}")
    
    return bandi

def main():
    """Scrape tutti i siti e salva in JSON"""
    print("🔄 Inizio scraping...")
    
    tutti_bandi = []
    tutti_bandi.extend(scrape_aria())
    tutti_bandi.extend(scrape_lombardia())
    tutti_bandi.extend(scrape_milano())
    tutti_bandi.extend(scrape_municipio2())
    
    print(f"✅ Trovati {len(tutti_bandi)} bandi")
    
    # Salva nel file
    with open('bandi.json', 'w', encoding='utf-8') as f:
        json.dump(tutti_bandi, f, indent=2, ensure_ascii=False)
    
    print("💾 Salvato in bandi.json")

if __name__ == '__main__':
    main()