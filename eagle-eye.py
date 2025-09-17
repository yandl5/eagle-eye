import feedparser
import hashlib
from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from waitress import serve

NEWS_SOURCES = {
    # Internacionais
    "KrebsOnSecurity": "https://krebsonsecurity.com/feed/",
    "The Hacker News": "https://thehackernews.com/feeds/posts/default",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "CSO Online": "https://www.csoonline.com/index.rss",
    "Wired Security": "https://www.wired.com/feed/category/security/latest/rss",
    "The Record": "https://therecord.media/category/cybersecurity/feed/",
    "ZDNet Security": "https://www.zdnet.com/topic/security/rss.xml",
    "Infosecurity Magazine": "https://www.infosecurity-magazine.com/rss/news/",

    # Brasileiros
    "Canaltech Security": "https://canaltech.com.br/feed/seguranca/",
    "Tecnoblog Security": "https://tecnoblog.net/feed/categoria/seguranca/",
    "Olhar Digital Security": "https://olhardigital.com.br/feed/categoria/seguranca/",
    "Pplware Brasil Security": "https://pplware.sapo.pt/feed/seguranca/"
}

def get_news(keyword):
    news = []
    seen = {}  # hash -> fontes

    for source, url in NEWS_SOURCES.items():
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"Erro ao ler feed {source}: {e}")
            continue

        for entry in feed.entries:
            try:
                title = getattr(entry, "title", None)
                link = getattr(entry, "link", None)

                if not title or not link:
                    continue

                if keyword.lower() in title.lower():
                    # hash do título (normalizado)
                    h = hashlib.md5(title.lower().encode()).hexdigest()

                    if h not in seen:
                        seen[h] = [source]
                    else:
                        seen[h].append(source)

                    news.append({
                        "title": title,
                        "link": link,
                        "source": source,
                        "hash": h
                    })
            except Exception as e:
                print(f"Erro ao processar notícia do feed {source}: {e}")
                continue

    # Se não encontrou notícias, adicionar placeholder
    if not news:
        news.append({
            "title": f"Nenhuma notícia encontrada para '{keyword}'",
            "link": "",
            "source": "N/A",
            "hash": "0",
            "trending": False,
            "sources": []
        })

    # adicionar info de duplicação
    for item in news:
        fontes = seen.get(item["hash"], [item["source"]])
        if len(fontes) > 1:
            item["trending"] = True
            item["sources"] = fontes
        else:
            item["trending"] = False
            item["sources"] = [item["source"]]

    return news

class CyberNewsService(ServiceBase):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def search_news(ctx, keyword):
        try:
            results = get_news(keyword)
            for r in results:
                if r["trending"]:
                    yield f"[TRENDING] {r['title']} (Fontes: {', '.join(r['sources'])}) -> {r['link']}"
                else:
                    yield f"{r['title']} ({r['source']}) -> {r['link']}"
        except Exception as e:
            yield f"Erro ao processar a busca: {e}"

application = Application(
    [CyberNewsService],
    tns="cybernews.soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    wsgi_app = WsgiApplication(application)
    print("SOAP service running at http://0.0.0.0:8000")
    serve(wsgi_app, host="0.0.0.0", port=8000)
