from bs4 import BeautifulSoup
from clldutils.path import walk
from number_parser import parse_number
import re

TABLE_IDENTIFIER = ["MsoTableGrid", "a", "MsoNormalTable"]
SKIP = [
    "How-to-view-EN.htm",
    "How-to-view-CH.htm",
    "problem.html",
    "index.html",
    "index_old.html",
    "eugenechan.htm",
    "home-Chinese.html",
    "home.html",
    "Comments-6-Oct-2008.htm",
    "blank.html",
    "navi.html",
    "Xu-Shixuan.htm",
    "Chinese-Readers.htm",
    # all files which have <ol type="A"> are overview pages:
    "African-Others.htm",
    "Afro-Asiatic.htm",
    "Algic.htm",
    "Altaic.htm",
    "American-North-Cent-Others.htm",
    "American-Others.htm",
    "American-South-Others.htm",
    "Arawakan.htm",
    "Australian.htm",
    "AustroAsiatic.htm",
    "Austronesian-Central.htm",
    "Austronesian-Eastern.htm",
    "Austronesian-Western.htm",
    "Austronesian.htm",
    "Barbacoan.htm",
    "Carib.htm",
    "Caucasian.htm",
    "Central-South-NewGuinea-Kutubuan.htm",
    "Chibchan.htm",
    "Choco.htm",
    "Dravidian.htm",
    "East-New-Guinea-Highlands.htm",
    "East-Papuan.htm",
    "Easternl Austronesian.htm",
    "Eskimo-Aleut.htm",
    "Euro-Asian-Others.htm",
    "Eyak-Athabaskan.htm",
    "Geelvink-Bay.htm",
    "Hokan.htm",
    "Huon-Finisterre.htm",
    "Indoeuro.htm",
    "Iroquoian.htm",
    "Jean-Ge.htm",
    "Kainantu-Goroka.htm",
    "Khoisan.htm",
    "Macro-Ge.htm",
    "Madang-Adelbert-Range.htm",
    "Mataco-Guaicuru.htm",
    "Matacoan.htm",
    "Mayan.htm",
    "Miao-Yao.htm",
    "Mixe-Zoque.htm",
    "Muskogean.htm",
    "Na-Dene.htm",
    "Niger-Congo-Adamawa.htm",
    "Niger-Congo-Atlantic.htm",
    "Niger-Congo-Benue-Congo.htm",
    "Niger-Congo-Grassfield.htm",
    "Niger-Congo-Gur.htm",
    "Niger-Congo-Kwa.htm",
    "Niger-Congo-Mande.htm",
    "Niger-Congo-Narrow-Bantu.htm",
    "Niger-Congo.htm",
    "Nilo-Saharan.htm",
    "Ok-Awyu.htm",
    "Oto-Manguean.htm",
    "Paezan.htm",
    "Panoan.htm",
    "Papuan-Others.htm",
    "Penutian.htm",
    "Quechuan.htm",
    "Ramu-Lower-Sepik.htm",
    "Salishan.htm",
    "Sepi-Ramu.htm",
    "Sepik-New.htm",
    "Sino-Tibetan.htm",
    "Siouan.htm",
    "South-Birds-Head-Timor-Alor-Pantar.htm",
    "Southeast-Papuan.htm",
    "Tacanan.htm",
    "Tai-Kadai.htm",
    "Tigrigna.htm",
    "Torricelli.htm",
    "Totonacan.htm",
    "Trans-Fly-Bulaka-River.htm",
    "Trans-New Guinea.htm",
    "Tucanoan.htm",
    "Tupi.htm",
    "Uralic.htm",
    "Uto-Aztecan.htm",
    "West-Papuan.htm",
    "West-Timor-Alor-Pantar.htm",
    "Westpapuan-Timor-Alor-Pantar.htm",
    "Witotoan.htm",
    "Yuman.htm",
    # skip duplicates found via MD5
    "Ache.htm",  # Iliun.htm
    "Aché.html",  # Ache-Tupi.html
    "Amarakaeri.htm",  # Batak-Toba.htm
    "Aymara.htm",  # Aymara-Central.htm
    "Baluan.htm",  # Baluan-Paluai.htm
    "Befang.htm",  # Befang-CM.htm
    "Casiguran Dumagat Agta.htm",  # Agta-Casiguran-Dumagat.htm
    "Cholim Tangsa.htm",  # Ngaimong-Cholim-Tangsa-Naga.htm
    "Dhivehi.htm",  # Dhivehi.html
    "EastFrisian.htm",  # EasttFrisian.html
    "East Yugur.htm",  # East-Yugur.htm
    "Guwot.htm",  # Guwot-Duwet.htm
    "Halh Mongolian.htm",  # Halh-Mongolian.htm
    "Jimi-Nigeria.html",  # Jimi-Nigeria.htm
    "Khamnigan Mongol.htm",  # Khamnigan-Mongol.htm
    "Kohistani Shina.html",  # Shina-Kohistani.htm
    "Kundal Shahi.htm",  # Kundal-Shahi.htm
    "Li-Meifu.htm",  # Li-Meifu-Qi-Tongzha.htm
    "Lishana Deni.htm",  # Challa-Lishana-Deni.htm
    "Mako.htm",  # Mako-Ve.htm
    "Manx.htm",  # ManxGaelic.htm
    "Mueshaungx Tangsa",  # Mueshaungx-Tangsa-Naga.htm
    "North Zhuang.htm",  # Zhuang-North.htm
    "Northern Khmer.htm",  # Northern-Khmer.htm
    "Phom Naga.htm",  # Phom-Naga.htm
    "Romagnolo.htm",  # Romagnol.htm
    "Rongshui Miao.htm",  # Rongshui-Miao.htm
    "Sa.htm",  # Sa-Vanuatu.htm
    "ScotsGaelic.htm",  # ScotGaelic.htm
    "Shiri Dargwa.html",  # Dargwa-Shiri.html
    "Sinhala.html",  # Sinhala.htm
    "Southern Rengma Naga.htm",  # Southern-Rengma-Naga.htm
    "Teanu-Buma.htm",  # Teanu.htm
    "Thangal Naga.htm",  # Thangal Naga.htm
    "Tsimané.htm",  # Tsimane.htm
    "Tundra Nenets.htm",  # Tundra-Nenets.htm
    "Upper Necaxa Totonac.htm",  # Totonac-Upper-Necaxa.htm
    "Yimgchungru Naga.htm",  # Yimchungru-Naga.htm
    "Yimgchungru-Naga.htm",  # Yimchungru-Naga.htm
    # not entirely identical but same lg title and only counterpart is linked in overview
    "Abenaki-Western.htm",  # Munsee.htm
    "Akawaio-2.htm",  # Akawaio.htm
    "Abenlen-Ayta.htm",  # Ayta-Abenlen.htm
    "Achuar.html",  # Hruso.html
    "Hruso.htm",  # Hruso.html
    "Zeme-Naga.htm",  # Zeme Naga.html
    "North-Ambrym.htm",  # Ambrym-North.htm
    "Amwi Khasi.htm",  # Khasi-Amwi.htm
    "Ao Naga.htm",  # Naga-Ao.htm
    "Apinayé.htm",  # Apinaye.htm
    "Asu-Pare.htm",  # Asu.htm
    "Banam Bay-Burmbar.htm",  # Ndenggan-BanamBay.htm
    "Bareke.htm",  # Vangunu-Bereke.htm
    "Dungra Bhil.htm",  # Bhil-Dungra.htm
    "Bhili.htm",  # Bhili-AhwaDangs.htm
    "Bhumij.htm",  # Mundari.htm
    "Buhinon Bikol.htm",  # Bikol-Buhinon.htm
    "Sarangani Bilaan.htm",  # Bilaan-Sarangani.htm
    "Bola.htm",  # Bola-AN.htm
    "Brooke's Point Palawano.htm",  # Palawano-Brookes-Point.htm
    "Bru-East.htm",  # Eastern-Bru.htm
    "Bugan.htm",  # Bugun-Khowa.htm
    "Buyang.htm",  # Buyang-Baha.htm
    "Buyang-Ecun.htm",  # Buyang-Baha.htm
    "Buyang-Langjia.htm",  # Buyang-Baha.htm
    "Cadong.htm",  # Chadong.htm
    "Chamchang-Kimsing-Naga.htm",  # Naga-Tangshang.htm
    "Kimsing.htm",  # Naga-Tangshang.htm
    "Chin-Asho.htm",  # Chin-Asho.html
    "Haka Chin.htm",  # Chin-Haka.htm
    "Thawr Chin.htm",  # Chin-Thawr.htm
    "Guanyinge Tuhua.htm",  # Chinese-Guanyinge.htm
    "Chinese-Waxiang.htm",  # Waxianghua.htm
    "Chinese-Wulinghua.htm",  # Wulinghua.htm
    "Cholim Tangsa.htm",  # Naga-Tangshang.htm
    "Ngaimong-Cholim-Tangsa-Naga.htm",  # Naga-Tangshang.htm
    "Cinda.htm",  # Cinda-Kamuku.htm
    "North-AlaskaInupiatun.htm",  # North-Alaskan-Inupiatun.htm
    "North Alaskan Inupiatun.htm",  # North-Alaskan-Inupiatun.htm
    "Covok.htm",  # Cuvok.htm
    "Dangaura Tharu.htm",  # DangauraTharu.htm
    "Dargwa-Shiri.htm",  # Dargwa-Shiri.html
    "Kotia.htm",  # Desiya.htm
    "Dogul-Dom Dogon.htm",  # Dogon-Dogul-Dom.htm
    "Tommo So Dogon.htm",  # Dogon-Dondum-Dom.htm
    "East Uvea.htm",  # Uvea-East-Wallisian.htm
    "Yugur-East.htm",  # East-Yugur.htm
    "Fijian-Namosi-Naitasiri.htm",  # Fijian-Gone-Dau.htm
    "Loloda.htm",  # Galela.htm
    "Ganga.htm",  # Ganda.htm
    "Garasia.htm",  # Kukna.htm
    "Gelao-Judu.htm",  # Gelao-Duoluo.htm
    "Greenlandic Inuktitut.htm",  # Greenlandic-Inuktitut.htm
    "Guduf-Gav.htm",  # Guduf-Gava.htm
    "Guwot.htm",  # Guwot-Duwet.htm
    "Gyarong-Japhug.htm",  # Jiarong.htm
    "Hakhun-Tangsa-Naga.htm",  # Naga-Tangshang.htm
    "Tase-Naga.htm",  # Naga-Tangshang.htm
    "Mongolian-Halh.htm",  # Halh-Mongolian.htm
    "Miao-Shuat.htm",  # Hmong-Shuat.htm
    "Huambisa.htm",  # Huambisa.html
    "Yesesiam.htm",  # Iresim-Yeresiam.htm
    "Jarawa.htm",  # Jarawa-India.htm
    "Jiarong-Zbu-2.htm",  # Jiarong-Zbu.htm
    "Kachama-Ganjule.htm",  # Kachama-Ganjule.html
    "KachiKoli.htm",  # KachiiKoli.htm
    "Qairaq-Kairak.htm",  # Kairak.htm
    "Kalagan.htm",  # Kalagan-Kagan.htm
    "Kalinga-Northern.htm",  # Kalinga-Northern.html
    "Karipuna.htm",  # Uru-eu-uau-uau.htm
    "Khmer-Northern.htm",  # Northern-Khmer.htm
    "Kholok.html",  # Kholok.htm
    "Kolami-Southeastern.htm",  # Kolami-Northwestern.htm
    "Komering.html",  # Komering.htm
    "Konda.htm",  # Konda-PNG.htm
    "Kuikúro.htm",  # Kuikuro.htm
    "Kullu Pahari.htm",  # Pahari-Kullu.htm
    "Kundal Shahi.htm",  # Kundal-Shahi.htm
    "Kung.htm",  # Kung-CM.htm
    "Li-Baoding.htm",  # Li-Baoding-Lauhut.htm
    "Li-Yaunmen.htm",  # Li-Yuanmen.htm
    "Lingurian.htm",  # Ligurian.htm
    "Lohorong.htm",  # Lorung-North.htm
    "Luba-Shaba.htm",  # Luba-Katanga.htm
    "Macushi.html",  # Macushi.htm
    "Western Bukidnon Manobo.htm",  # Manobo-Western-Bukidnon.htm
    "Marghi-South.htm",  # South Marghi.html
    "Marwari.htm",  # MarwariBhil.htm
    "Mawé.htm",  # Satere-Mawe.htm
    "Ngamay.htm",  # Mbay.htm
    "Mogum.htm",  # Mogum.html
    "Nek.htm",  # Nek-PNG.htm
    "Nisa.htm",  # Sauri.htm
    "Nong Zhuang.htm",  # Zhuang-Nong.htm
    "Northwestern Ojibwa.htm",  # Ojibwa-Northwestern.htm
    "Wa.htm",  # Parauk.htm
    "Southern Pashtu.htm",  # Pashtu-Southern.htm
    "Phom Naga.htm",  # Phom-Naga.htm
    "Pintiini.htm",  # Pintiini-Wangkatja.htm
    "Pumé.html",  # Pume-Ven.htm
    "Pumi-North-Old.htm",  # Pumi-North.htm
    "Riang.htm",  # Riang-Sak.htm
    "S-Rengma-Naga.htm",  # Southern-Rengma-Naga.htm
    "Saliba.htm",  # Saliba-PNG.htm
    "Salish-Straits-Northern.htm",  # Salish-Straits.htm
    "Southern Sama.htm",  # Sama-Southern.htm
    "Tina Sambal.htm",  # Sambal-Tina.htm
    "Siar-Lak.htm",  # Siar.htm
    "Sibe.htm",  # Sibe-PNG.htm
    "Tai Lu.htm",  # Tai-Lu.htm
    "Tera-Chadic.htm",  # Tera.htm
    "Thangal Naga.htm",  # Thangal-Naga.htm
    "Tohono-Oodham-Papago.htm",  # Tohono O'odham-Papago.htm
    "Tupari.htm",  # Tupari-Adamawa.htm
    "Yang Zhuang.htm",  # Zhuang-Yang.htm
    "Yanggao-Miao.htm",  # Yanghao-Miao.htm
    "Yau-PNG.htm",  # Yau-Morobe.htm
    "Yau-PNG.htm",  # Yau-Morobe.htm
    "Yucuna.htm",  # Yucuna.html
    "Sakirabia.htm",  # Sakirabia-Mekens.htm
    "Mawe.htm",  # Satere-Mawe.htm
    ]
SKIP_RE = re.compile(r"(?i)question")

ETHNOLOGUE = re.compile(r"(:?(http[s]?://)?www|archive)\.ethnologue\.(?:com|org)/", re.IGNORECASE)

CODE_PATTERNS = [
    re.compile("code=(?P<code>[a-zA-Z]{3})"),
    re.compile("language/(?P<code>[a-zA-Z]{3})"),
]

TITLE_PATTERNS = [
    re.compile(r"language\s+name\s+and\s+locatii?on\s*\S\s*(?P<name>.+?)\s*\[", flags=re.I),
    re.compile(r"language\s+name\s+and\s+locatii?on\s*\S\s*(?P<name>.+?)\s*Ref", flags=re.I),
    re.compile(r"language\s+name\s+and\s+locatii?on\s*\S\s*(?P<name>.+?) {3,}", flags=re.I),
    re.compile(r"language\s+name\s+and\s+locatii?on\s*\S\s*(?P<name>.+?)\s*$", flags=re.I),
]

CONTRIB_PATTERNS = [
    re.compile(r"linguists?\s+providing\s+data\s+and\s+date\s*\S\s*(?P<name>.+?)\s*(提供|语言|资料)", flags=re.I),
    re.compile(r"linguists?\s+providing\s+data\s+and\s+date\s*\S\s*(?P<name>.+?)\s*$", flags=re.I),
    re.compile(r"data\s+source\s*\S\s*(?P<name>.+?)\s*(提供|语言|资料)", flags=re.I),
    re.compile(r"source\s*\S\s*(?P<name>.+?)\s*(提供|语言|资料)", flags=re.I),
    re.compile(r"data\s+source\s*\S\s*(?P<name>.+?)\s*$", flags=re.I),
    re.compile(r"source\s*\S\s*(?P<name>.+?)\s*$", flags=re.I),
]

SYSTEM_PATTERNS = [
    re.compile(r"has\s+a\s+(?P<name>[^\.’%]+?)\s*((numeral\s+)?systems?)[\s,\.]+(?!(up|base|with))", flags=re.I),
    re.compile(r"(is|system)\s+based\s+on\s+((a|the)\s+)?(?P<name>['\w\d]+?)[\.;]", flags=re.I),
    re.compile(r"have\s+a\s+(?P<name>[^\.’%]+?)\s*((numeral\s+)?systems?)[\s,\.]+(?!(up|base|with))", flags=re.I),
    re.compile(r"system\s+is\s+(?P<name>decimal|deciaml|bianary|vige(s|c)imal|quintenary|quinary\-decimal|quinary\-vigesimal|quinary|binary)", flags=re.I),
]

COMMENT_PATTERNS = [
    re.compile(r"other\s+comments?\s*\S\s*(?P<name>.+?)\s*$", flags=re.I),
]


def get_file_paths(raw_htmls, n=None):
    """
    Build a sorted list of PosixPath() objects for all files in the specified
    directory, e.g. numerals/raw/, skipping files defined in SKIP and as SKIP_RE.
    :param raw_htmls: Path to raw numerals HTML files.
    :param n: How many HTML files to process, useful for debugging.
    :return: A list of PosixPath() objects with path information for the files.
    """
    if n:
        return sorted(
            [f for f in walk(raw_htmls) if
                f.suffix.startswith(".htm") and
                not f.name.startswith("Copy of") and
                f.name not in SKIP and
                not re.search(SKIP_RE, f.name)]
        )[:n]
    else:
        return sorted(
            [f for f in walk(raw_htmls) if
                f.suffix.startswith(".htm") and
                not f.name.startswith("Copy of") and
                f.name not in SKIP and
                not re.search(SKIP_RE, f.name)]
        )


def find_tables(file_paths):
    """
    Find all tables defined by TABLE_IDENTIFIER in file_paths.
    :param file_paths: A list of PosixPath() objects containing path information
    for the numerals HTML files.
    :return: A generator with pairs of (LanguageName, ResultSet). If ResultSet
    is empty, there was no table defined in TABLE_IDENTIFIER in the
    corresponding HTML file.
    """
    for f in file_paths:
        parsed = BeautifulSoup(f.read_text(), "html.parser")
        sf_names = []
        contributors = []
        comments = []
        bases = []
        all_tables = parsed.find_all("table", {"class": TABLE_IDENTIFIER})
        for tbl in all_tables:
            t = re.sub(r'[\n\r\t ]+', ' ', tbl.get_text())
            for pattern in TITLE_PATTERNS:
                m = pattern.search(t)
                if m:
                    if len(sf_names):
                        if len(contributors) < len(sf_names):
                            contributors.append('')
                        if len(comments) < len(sf_names):
                            comments.append('')
                        if len(bases) < len(sf_names):
                            bases.append('')
                    n = re.sub(r' {2,}', ' ', m.group("name")).strip()
                    sf_names.append(re.sub(r'\s*,$', '', n))
                    break
            for pattern in CONTRIB_PATTERNS:
                m = pattern.search(t)
                if m:
                    n = re.sub(r' {2,}', ' ', m.group("name")).strip()
                    n = n.replace("提供", "")
                    contributors.append(n)
                    break
            for pattern in COMMENT_PATTERNS:
                m = pattern.search(t)
                if m:
                    n = re.sub(r' {2,}', ' ', m.group("name")).strip()
                    comments.append(n)
                    break
            for pattern in SYSTEM_PATTERNS:
                m = pattern.search(t)
                if m:
                    n = re.sub(r' {2,}', ' ', m.group("name")).strip()
                    n = re.sub(r"\s*(numerals?|number|traditional|typical|well\-developed|simple|base|cou(n|r)ting|rather|')\s*", '', n, flags=re.I)
                    n = n.replace("deciaml", "decimal").replace("bianary", "binary").replace("vigecimal", "vigesimal")
                    if len(n) < 20:
                        bases.append(n)
                    else:
                        bases.append('')
                    break

        if len(sf_names):
            if len(contributors) < len(sf_names):
                contributors.append('')
            if len(comments) < len(sf_names):
                comments.append('')
            if len(bases) < len(sf_names):
                bases.append('')

        if len(sf_names) != len(contributors) and len(sf_names) != len(bases) and\
                len(sf_names) != len(comments):
            comments = ["CHECK: %s" % (c) for c in comments]

        yield (f.stem, all_tables, f.name, sf_names, contributors, bases, comments)


def find_number_table(table):
    """
    A helper function to identify tables containing number information so that
    we don't have to rely on the (implicit) ordering of tables within the HTML
    files.
    :param table: The tables from a ResultSet to be processed.
    :return: True if number table (>= 1 numerals), False otherwise.
    """
    numbers = []

    for element in table:
        try:
            # We collect all potential numbers in a list and simply check
            # the length of the list at the end.
            numbers.append(parse_number(element))
        except ValueError:
            pass

    if len(numbers):
        return True
    else:
        return False


def parse_table(table):
    """
    A helper function to parse tables into a list of strings. This used to
    make identifying tables containing numerals easier.
    :param table: A numerals HTML table.
    :return: A list of strings with the elements and other literal information.
    """
    table_elements = table.find_all("tr")
    elements = []

    for row in table_elements:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]

        for ele in cols:
            if ele:
                elements.append(ele)

    return elements


def iterate_tables(tables):
    number_tables = []
    other_tables = []

    for table in tables:
        parsed_table = parse_table(table)

        if find_number_table(parsed_table) is True:
            number_tables.append(parsed_table)
        else:
            other_tables.append(table)

    return number_tables, other_tables


def find_ethnologue_codes(tables):
    """
    Takes a set of tables (preferably other_tables from a NumeralsEntry object)
    and tries to find Ethnologue links and their corresponding codes for better
    matching of Glottocodes.
    :param tables: A set of tables (or a single table) from parsing a numerals
    HTML entry.
    :return: A list of Ethnologue codes found on the respective site.
    """
    ethnologue_codes = []

    for table in tables:
        link = table.find("a", href=ETHNOLOGUE)
        if link:
            for pattern in CODE_PATTERNS:
                m = pattern.search(link["href"])
                if m:
                    ethnologue_codes.append(m.group("code").lower())
                    break
            else:
                print(link["href"])

    return ethnologue_codes
