import requests
import socks
import socket
import urwid
import json
import time
import threading
import csv
import random
import sys
from tqdm import tqdm
from bs4 import BeautifulSoup

# Proxy settings
USE_CUSTOM_PROXIES = True  # Set to False to use default Tor proxy
CUSTOM_PROXIES = []

DEFAULT_PROXY = ("127.0.0.1", 9050)

def load_proxies(filename="proxy.txt"):
    try:
        with open(filename, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        return [(p.split(":")[0], int(p.split(":")[1])) for p in proxies if ":" in p]
    except Exception as e:
        print(f"⚠ Error loading proxies: {e}")
        return []

CUSTOM_PROXIES = load_proxies()

def set_proxy():
    if USE_CUSTOM_PROXIES and CUSTOM_PROXIES:
        ip, port = random.choice(CUSTOM_PROXIES)
    else:
        ip, port = DEFAULT_PROXY
    socks.set_default_proxy(socks.SOCKS5, ip, port)
    socket.socket = socks.socksocket

set_proxy()

# User-Agent List for Spoofing
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Predefined Dark Web Search Engines
PREDEFINED_SEARCH_ENGINES = [
    "http://ahmia.fi/",
    "http://tordex5tm4gqz4s3.onion/",
    "http://rqkz2zcavqlzu32e.onion/",
    "http://candlewo5j7suw.onion/",
    "http://tor66sezptuu2xsw.onion/",
    "http://darksearch.io/",
    "http://onionlandsearchengine.onion/",
    "http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/",
    "http://deepsearchwwuw5qsc.onion/",
    "http://notevil.xyz/",
    "http://3g2upl4pq6kufc4m.onion/",
    "http://xmh57jrzrnw6insl.onion/",
    "http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page",
    "http://32rfckwuorlf4dlv.onion/",
    "http://e266al32vpuorbyg.onion/bookmarks.php",
    "http://5plvrsgydwy2sgce.onion/",
    "http://2vlqpcqpjlhmd5r2.onion/",
    "http://nlmymchrmnlmbnii.onion/",
    "http://kpynyvym6xqi7wz2.onion/links.html",
    "http://wiki5kauuihowqi5.onion/",
    "http://torwikignoueupfm.onion/index.php?title=Main_Page",
    "http://kpvz7ki2v5agwt35.onion",
    "http://idnxcnkne4qt76tg.onion/",
    "http://torlinkbgs6aabns.onion/",
    "http://jh32yv5zgayyyts3.onion/",
    "http://wikitjerrta4qgz4.onion/",
    "http://xdagknwjc7aaytzh.onion/",
    "http://3fyb44wdhnd2ghhl.onion/",
    "http://j6im4v42ur6dpic3.onion",
    "http://p3igkncehackjtib.onion/",
    "http://kbhpodhnfxl3clb4.onion",
    "http://cipollatnumrrahd.onion/",
    "http://wvk32thojln4gpp4.onion/wiki/index.php/",
    "http://world6zlyzbs6yol36h6wjdzxddsnos3b4rakizkm3q75dwkiujyauid.onion/register_now",
    "http://darkmarketsomqvzqfjudpd6t5eabgvvpplrbtzq6prervyogenlrlqd.onion/signup/MFPSCQ",
    "http://f3dxwzcmojrlphehqwcecwe3amg6rkzgilcn4xqxmaiezoedijf6rtid.onion/register/NOlF",
    "http://worldps45uh3rhedmx7g3jgjf3vw52wkvvcastfm46fzrpwoc7f33lid.onion/register_now",
    "http://lstkx6p3gzsgfwsqpntlv7tv4tsjzziwp76gvkaxx2mqe3whvlp243id.onion/register/NOlF",
    "http://worldtx2zjdrxwwdvthuilhadqyfcl3fqgyjddhtakq3j4fonppvy3id.onion/register_now",
    "http://asap2u4pvplnkzl7ecle45wajojnftja45wvovl3jrvhangeyq67ziid.onion",
    "http://coronhls55k7oo3mzzwf3xlketww6rgdpxtpoxv3yogtvjiboohytuqd.onion/i/s6bl6ybntes60i8fwyxssy4y/",
    "http://p5eg3xsssjglu6tvwfazp2nqqwfpah55wr3ljil2bezp5shix5ruqsqd.onion/register/N1W8U58H",
    "http://worldgyonnnlgg332jwgjxvj2dojerz2hh65ce44h56howcfmpehupad.onion/register_now",
    "http://yxuy5oau7nugw4kpb4lclrqdbixp3wvc4iuiad23ebyp2q3gx7rtrgqd.onion/register/NOlF",
    "http://coronjisa5cawck7ggbs6sln25mvosm6gftbikhrohybtca3oqcih2id.onion/i/s6bl6ybntes60i8fwyxssy4y/",
    "http://57d5j6hfzfpsfev6c7f5ltney5xahudevvttfmw4lrtkt42iqdrkxmqd.onion/register/N1W8U58H",
    "http://557ssqsc5py54w7ofwnlw2j2guohklywb52ymfw5v6glbyibqravwkyd.onion/register/N1W8U58H",
    "http://4xt3tygdbhijffgafkpyvzyftpmtq75w5kgch3emkb5c7mjii462klid.onion/register/N1W8U58H",
    "http://gykafhjweddhrbm5zn6zwi5gwxd3zzdjjiqxx7ebp27b4xpf3b2lggad.onion/register/N1W8U58H",
    "http://ste6sk22hcb76kw5hkyp2czf6nerj56lgvufkcpj6olx4v5mlqhri4id.onion/register/N1W8U58H",
    "http://darkzzx4avcsuofgfez5zq75cqc4mprjvfqywo45dfcaxrwqg6qrlfid.onion",
    "http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion",
    "http://recon222tttn4ob7ujdhbn3s4gjre7netvzybuvbq2bcqwltkiqinhad.onion",
    "http://envoys5appps3bin.onion",
    "http://envoyvvcccvepc5i.onion",
    "http://envoyzlbxpgniels.onion",
    "http://thehub7xbw4dc5r2.onion",
    "http://talismanrestz7mr.onion",
    "http://nzlbyrcvvqtrkxiu.onion",
    "http://2oywvwmtzdelmiei.onion",
    "http://dnmugu4755642434.onion",
    "http://monopolyberbucxu.onion",
    "http://auzbdiguv5qtp37xoma3n4xfch62duxtdiu4cfrrwbxgckipd4aktxid.onion",
    "http://7yipwxdv5cfdjfpjztiz7sv2jlzzjuepmxy4mtlvuaojejwhg3zhliqd.onion",
    "http://cieprrpdgp7moka2ktlwy54ooymtgsre23enrf4dfzssap74zz45f6id.onion",
    "http://pqqmr3p3tppwqvvapi6fa7jowrehgd36ct6lzr26qqormaqvh6gt4jyd.onion",
    "http://q2f7swt5yvbhciqqbbsidufu2vtkv6ivwy6g5i5ukejjlb2jeghd2had.onion",
    "http://imperiyakggyacaf.onion",
    "http://asap2u4pvplnkzl7ecle45wajojnftja45wvovl3jrvhangeyq67ziid.onion",
    "http://cannahome3ke3366.onion",
    "http://cannahomekql6hhg.onion",
    "http://cannazonceujdye3.onion",
    "http://sxwjdzct7jnoef7o.onion",
    "http://7ympuwybhdedjddibndoroyur3frvc27bo5ipicgozywejsdq7wvvbqd.onion",
    "http://57iwpifn5xr7bim3lm4lywjuz45za4cbwusyerh362jiqnoraijzh2id.onion",
    "http://cannazon4gbjluus.onion",
    "http://invicus3w24e22upa4scshje3e5rxqjjv4hf7l7p6lckzkukylsewwid.onion",
    "http://televenkzhxxxe6sw4fntkm4csj6s4csqkuczqhrz6aw7ae3me2tjlyd.onion",
    "http://yxuy5oau7nugw4kpb4lclrqdbixp3wvc4iuiad23ebyp2q3gx7rtrgqd.onion",
    "http://333f7gpuishjximodvynnoisxujicgwaetzywgkxoxuje5ph3qyqjuid.onion",
    "http://tt2mopgckifmberr.onion",
    "http://rrlm2f22lpqgfhyydqkxxzv6snwo5qvc2krjt2q557l7z4te7fsvhbid.onion",
    "http://darkoddrkj3gqz7ke7nyjfkh7o72hlvr44uz5zl2xrapna4tribuorqd.onion",
    "http://hydraruzxpnew4af.onion",
    "http://exploitinqx4sjro.onion",
    "http://verified2ebdpvms.onion",
    "http://canadahq2lo3logs.onion",
    "http://canadahqx53lcurj.onion",
    "http://germanyruvvy2tcw.onion",
    "http://2x4tmsirlqvqmwdz.onion",
    "http://wannabuyaynozvmz.onion",
    "http://lgh3eosuqrrtvwx3s4nurujcqrm53ba5vqsbim5k5ntdpo33qkl7buyd.onion",
    "http://bbcnewsv2vjtpsuy.onion",
    "http://bitmailendavkbec.onion",
    "http://dwnewsvdyyiamwnp.onion",
    "http://pornhubthbh7ap3u.onion",
    "http://propub3r6espa33w.onion",
    "https://protonirockerxow.onion",
    "http://nzh3fv6jc6jskki3.onion",
    "http://zsolxunfmbfuq7wf.onion",
    "http://j6uhdvbhz74oefxf.onion",
    "http://ijeeynrc6x2uy5ob.onion",
    "https://nytimes3xbfgragh.onion",
    "http://torbox3uiot6wchz.onion",
    "http://lpiyu33yusoalp5kh3f4hak2so2sjjvjw5ykyvu2dulzosgvuffq6sad.onion",
    "http://agoradeska6jfxpf.onion",
    "http://localmonerogt7be.onion",
    "http://expyuzz4wqqyqhjn.onion",
    "http://xmrguide42y34onq.onion",
    "http://stormgm7blbk7odd.onion",
    "http://dtmfiovjh42uviqez6qn75igbagtiyo724hy3rdxm77dy2m5tt7lbaqd.onion",
    "http://xcln5hkbriyklr6n.onion",
    "http://njalladnspotetti.onion",
    "http://archivecaslytosk.onion",
    "https://3g2upl4pq6kufc4m.onion",
    "https://facebookcorewwwi.onion",
    "http://fncuwbiisyh6ak3i.onion",
    "http://psychonaut3z5aoz.onion",
    "http://oxwugzccvk3dk6tj.onion",
    "http://jthnx5wyvjvzsxtu.onion",
    "http://enxx3byspwsdo446jujc52ucy2pf5urdbhqw3kbsfhlfjwmbpj5smdad.onion",
    "http://endchan5doxvprs5.onion",
    "http://s6424n4x4bsmqs27.onion",
    "http://ddosecretspzwfy7.onion",
    "http://secmailw453j7piv.onion",
    "https://coinpaymtstgtibr.onion",
    "http://jirk5u4osbsr34t5.onion",
    "http://suprbayoubiexnmp.onion",
    "http://wlupld3ptjvsgwqw.onion",
    "http://wlchatc3pjwpli5r.onion",
    "http://chronosu3ulk3o3a.onion",
    "http://tapeucwutvne7l5o.onion",
    "http://politiepcvh42eav.onion",
    "http://ciadotgov4sjwlzihbbgxnqg3xiyrg7so2r2o3lt5wz5ypk4sxyjstad.onion",
    "http://ncidetf3j26mdtvf.onion",
    "http://darkfailllnkf4vf.onion",
    "http://worldehc62cgugrgj7oc76tcna45fme47oqjrei4d4aa7xorw7fyvcyd.onion/register_now",
    "http://mgybzfrldjn5drzv537skh7kgwgbq45dwha67r4elda4vl7m6qul5xqd.onion",
    "http://castlee5janmtc5h6jiorit7lzdhgfuy43po4oddgi3qpm52ljyljyyd.onion/register/DriveDeep",
    "http://underdjyvfav2wpl.onion/crawler",
    "http://rlujtxikez5kicwj.onion/",
    "http://onionlnkooppcbrs.onion/",
    "http://jpe6qltxg6am3jwk.onion/",
    "http://wj3hovv2rpsrtwtx.onion/",
    "http://searcherc3uwk535.onion/",
    "http://darkweb2zz7etehx.onion/",
    "http://deeplinkdeatbml7.onion/index.php",
    "http://torlinksd6pdnihy.onion/",
    "http://aidenm7chl2xypu4.onion/links/",
    "http://vwx4mjvwoszgnagzcrwdjlsq3pq3zyob3zpq5qissxdoivnuyylzn7yd.onion/",
    "http://onionsearh6bygec.onion/",
    "http://darkdirmpmoq3uur.onion",
    "http://zdxgqrvvvpwnuj2n.onion/",
    "http://osearchxmn2zkycl.onion/",
    "http://godnotordyhrk4fs.onion/",
    "http://gjobqjj7zecwiqdl.onion/",
    "http://cregan3gnq6spjeb.onion/",
    "http://dlggj2krbqzm5dru.onion",
    "http://7nf5wkubzpodrezj.onion",
    "http://deepnetm3ygx2kd6.onion/",
    "http://uebff7g6dfuoupfl.onion/all/",
    "http://darkjdlh7yoy53ij.onion//",
    "http://oqwc4xrfgysdgw52tercv56vl2tfk5u7r6dspr2g2mwsj3dvb7zef4id.onion/",
    "http://7nf5wkubzpodrezj.onion/osiris_sites.html",
    "http://hss3uro2hsxfogfq.onion",
    "http://zlal32teyptf4tvi.onion/",
    "http://hell66nsdnoyx4bp.onion/yes/7261696e/",
    "http://fghecxysnrtpkyrb.onion/",
    "http://depastedihrn3jtw.onion/",
    "http://happenedpghnqffa.onion/",
    "http://armdzvcnd63t3k2i.onion/chat.php",
    "http://armdzvcnd63t3k2i.onion/",
    "http://hackerw6dcplg3ej.onion",
    "http://po5oi3bw7m5mvgf2.onion/",
    "http://i62zkc7k6kz7yw7p.onion/",
    "http://6l244unykianuo5a.onion/",
    "http://ib7yeggizt65x4qm.onion/",
    "http://linkdirdgrhkr2zm.onion/",
    "http://22222222nh2uah4n.onion/",
    "http://ow24et3lmhnqk64k.onion/",
    "http://kevinwangd2hcp4c.onion/blog",
    "http://rqkz2zcavqlzu32e.onion/"  
]

# Smart filtering keywords
SPAM_KEYWORDS = ["rehu"]

def check_tor_connection():
    try:
        response = requests.get("http://check.torproject.org", timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})
        if "Congratulations" in response.text:
            return "✔ Tor is working correctly!"
        else:
            return "❌ Tor is not working properly!"
    except Exception as e:
        return f"⚠ Error checking Tor connection: {e}"

def load_search_engines(filename="search_engines.txt"):
    try:
        with open(filename, "r") as f:
            engines = list(set([line.strip() for line in f if line.strip() and not line.startswith("#")]))
        return list(set(engines + PREDEFINED_SEARCH_ENGINES))  # Merge and remove duplicates
    except Exception as e:
        return PREDEFINED_SEARCH_ENGINES

def save_search_engine(url, filename="search_engines.txt"):
    try:
        with open(filename, "r") as f:
            existing_engines = set(f.read().splitlines())
        if url not in existing_engines:
            with open(filename, "a") as f:
                f.write(url + "\n")
    except Exception as e:
        pass

def search_interface():
    def start_search(button, user_input):
        keyword = edit_box.get_edit_text()
        if not keyword:
            keyword = random.choice(["marketplace", "forum", "services", "news", "drugs", "hacking"])
        results.set_text(f"🔍 Searching for: {keyword}...\n")
        start_scraping(keyword)
        results.set_text("✅ Search complete. Check results in darkweb_results.json and darkweb_results.csv")
    
    tor_status = check_tor_connection()
    title = urwid.Text(("banner", "💀 Dark Web Scraper - Tails OS Optimized 💀"), align='center')
    tor_status_text = urwid.Text(tor_status, align='center')
    edit_box = urwid.Edit("Enter keyword to search: ")
    search_button = urwid.Button("🔍 Start Search")
    urwid.connect_signal(search_button, 'click', start_search, edit_box)
    results = urwid.Text("", align='left')
    
    listbox_content = [
        title, urwid.Divider(), tor_status_text, urwid.Divider(),
        edit_box, urwid.Divider(),
        search_button, urwid.Divider(), results
    ]
    listbox = urwid.ListBox(urwid.SimpleFocusListWalker(listbox_content))
    return listbox

def start_ui():
    palette = [("banner", "light cyan", "black")]
    loop = urwid.MainLoop(search_interface(), palette)
    loop.run()

def start_scraping(keyword):
    search_engines = load_search_engines()
    if not search_engines:
        return
    results = []
    threads = []
    for engine in search_engines:
        set_proxy()  # Change proxy for each search engine request
        thread = threading.Thread(target=scrape_search_engine, args=(engine, keyword, results))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    with open("darkweb_results.json", "w") as f:
        json.dump(results, f, indent=4)

def scrape_search_engine(search_url, keyword, results):
    try:
        response = requests.get(search_url, timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href and ".onion" in href:
                    full_url = href if href.startswith("http") else "http://" + href
                    results.append({"Dark Web Link": full_url})
    except Exception:
        pass

def main():
    start_ui()

if __name__ == "__main__":
    main()
