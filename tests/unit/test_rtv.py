# import pathlib
import pytest
import rtvslo.rtv
import tests.data.povezave


@pytest.mark.parametrize("povezava", tests.data.povezave.delujoče)
def test_preveri_html_povezavo(povezava):
    assert rtvslo.rtv.Posnetek.preveri_html_povezavo(povezava) is True


@pytest.mark.parametrize("povezava", tests.data.povezave.neustrezne)
def test_preveri_html_neustrezne(povezava):
    assert rtvslo.rtv.Posnetek.preveri_html_povezavo(povezava) is None


@pytest.mark.parametrize("povezava", tests.data.povezave.napačne)
def test_preveri_html_napačne(povezava):
    assert rtvslo.rtv.Posnetek.preveri_html_povezavo(povezava) is None


@pytest.mark.parametrize("povezava", tests.data.povezave.delujoče)
def test_razberi_številko(povezava):
    posnetek = rtvslo.rtv.Posnetek(povezava)
    številka = posnetek.razberi_številko()
    assert type(številka) is str
    assert len(številka) == 9


@pytest.mark.parametrize("povezava", tests.data.povezave.neustrezne)
def test_preveri_html_povezavo_neustrezne(povezava):
    assert rtvslo.rtv.Posnetek.preveri_html_povezavo(povezava) is None


@pytest.mark.parametrize("povezava", tests.data.povezave.neustrezne)
def test_razberi_številko_neustrezne(povezava):
    posnetek = rtvslo.rtv.Posnetek(povezava)
    assert posnetek.razberi_številko() is None


@pytest.mark.parametrize("povezava", tests.data.povezave.napačne_fail)
def test_razberi_številko_napačne(povezava):
    posnetek = rtvslo.rtv.Posnetek(povezava)
    assert posnetek.razberi_številko() is str


@pytest.fixture
def posnetek():
    return rtvslo.rtv.Posnetek("")


# 4d #########################################################################


@pytest.fixture
def džejsn_4d():
    """
    109826798.json
    """
    return r'{"response":{"thumbnail_sec":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1.jpg","source":"SLO1","linkedShows":[],"description":"Dokumentarna oddaja, 3., zadnji del","broadcastDate":"2011-07-05 17:30:00","id":109826798,"recordingDate":"2011-07-05 17:30:00","payTv":[],"expirationDate":"3001-01-01 00:00:00","showDescription":"Zavod za gluhe in naglušne Ljubljana, osrednja državna ustanova za vzgojo, izobraževanje in specialno pedagoško obravnavo gluhih in naglušnih otrok in mladostnikov ter oseb z govorno- jezikovnimi motnjami je praznoval 110. obletnico delovanja. Pesnik Tone Pavček je gojencem in sodelavcem ZGNL ob tej priložnosti spesnil praznično pesem:\r\n»Duh ni nikoli gluh,\r\nkamor želi si, sega,\r\ns prsti lomi besedni kruh in glagol ŽIVETI sprega.«\r\nOb tej priložnosti so nastale v Izobraževalnem programu nacionalne televizije tri dokumentarno-izobraževalne oddaje, v katerih so predstavljene dejavnosti Zavoda, ki izobražuje in vzgaja otroke in mladostnike od obdobja, ko je njihova motnja diagnosticirana, do zaključka izobraževanja na srednji šoli. Specialni pedagogi in vzgojitelji želijo doseči optimalen razvoj otrokovih sposobnosti na vseh področjih izobraževanja, poseben poudarek pa namenjajo razvoju jezika (slovenskega in slovenskega znakovnega jezika), komunikacije sluha in govora. Z najmlajšimi v vrtcu in osnovni šoli, z mladostniki v srednji šoli (edini srednji šoli za gluhe in naglušne v Sloveniji) in tudi odraslimi v okviru dejavnosti, ki jih Zavod vodi v Zdravstveni enoti tudi v širšem slovenskem okolju.\r\nVse te dejavnosti na različnih stopnjah šolanja so predstavljene v oddajah, ki so posebne tudi zaradi skrbne popolne opreme sleherne od njih. S podnapisi, evropsko standardizirano optimalno velikostjo podobe tolmača s kretanjem vsega govorjenega besedila in odprtim sodelovanjem učencev in strokovnih sodelavcev Zavoda za gluhe in naglušne Ljubljana pri nastajanju dokumentarcev. Zato le-ti odsevajo prijazno okolje, nasmejane utrinke življenja v vrtcu, šoli, prostorih prostočasovnih dejavnosti od knjižnice, do telovadnice in igralnic.","showId":"173250539","publishDate":"1991-01-01 00:00:00","showTypeId":33,"mediaType":"video","title":"Ljubica Podboršek, dobra vila slovenskega znakovnega jezika","showName":"Meje mojega jezika niso meje mojega sveta","jwt":"u6_tipF6VscwzDpzOOGhjifQwo_QaxmXw8j4ElJFiGc","broadcast":{"genre":[],"genreIds":[]},"broadcastDates":[],"duration":1959,"images":{"orig":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1.jpg","fp1":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1_fp1.jpg","fp2":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1_fp2.jpg","fp3":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1_fp3.jpg","thumb":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1_thumb.jpg","show":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1_show.jpg","wide1":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1_wide1.jpg","wide2":"https://img.rtvcdn.si/_up/ava/ava_misc/channel_logos/SLO1_wide2.jpg"},"length_min":32,"length_h":"32:39","length":"00:32:39","date":"05.07.2011","date_slo":"5. 7. 2011","stub":"meje-mojega-jezika-niso-meje-mojega-sveta","link":"https://4d.rtvslo.si/arhiv/meje-mojega-jezika-niso-meje-mojega-sveta/109826798","showLink":"https://4d.rtvslo.si/oddaja/meje-mojega-jezika-niso-meje-mojega-sveta/173250539","showLinkBySource":"https://www.rtvslo.si/tv/oddaja/meje-mojega-jezika-niso-meje-mojega-sveta/173250539","canonical":{"domain":"https://365.rtvslo.si","path":"/arhiv/meje-mojega-jezika-niso-meje-mojega-sveta/109826798"},"show_stats":0,"user_ip":"93.103.250.36","user_id":false,"broadcastDisc":0}}'


@pytest.fixture
def džejsn_api_4d():
    return r'{"response":{"mediaFiles":[{"id":109826802,"streams":{"hls":"http://vodstr.rtvslo.si/encrypted00/_definst_/2011/07/05/MejemojegajezikanisomejemojegasvetaLjubicaPodborsekx201107051805x700000x351x413x.mp4/playlist.m3u8?keylockhash=NS5DrxHHXUa3mHOmrp4IFz5HQm1aH5E6tS2nnh7UdpM","http":"http://progressive.rtvslo.si/encrypted00/2011/07/05/MejemojegajezikanisomejemojegasvetaLjubicaPodborsekx201107051805x700000x351x413x.mp4?keylockhash=gcdYMFv5n-VTFQRyx7f_vtfai9u844NEoYC2Mv0JWPw","mpeg-dash":"http://vodstr.rtvslo.si/encrypted00/_definst_/2011/07/05/MejemojegajezikanisomejemojegasvetaLjubicaPodborsekx201107051805x700000x351x413x.mp4/manifest.mpd?keylockhash=NS5DrxHHXUa3mHOmrp4IFz5HQm1aH5E6tS2nnh7UdpM","hls_sec":"https://vodstr.rtvslo.si/encrypted00/_definst_/2011/07/05/MejemojegajezikanisomejemojegasvetaLjubicaPodborsekx201107051805x700000x351x413x.mp4/playlist.m3u8?keylockhash=NS5DrxHHXUa3mHOmrp4IFz5HQm1aH5E6tS2nnh7UdpM"},"mediaType":"MP4","bitrate":700000,"width":351,"height":413,"filesize":0}],"mediaFiles_sl":[]}}'


@pytest.fixture
def povezava_do_posnetka_4d():
    """
    http
    ostale: hls, mpeg-dash, hls-sec
    """
    return r'http://progressive.rtvslo.si/encrypted00/2011/07/05/MejemojegajezikanisomejemojegasvetaLjubicaPodborsekx201107051805x700000x351x413x.mp4?keylockhash=gcdYMFv5n-VTFQRyx7f_vtfai9u844NEoYC2Mv0JWPw'


@pytest.fixture
def jwt_4d():
    return "u6_tipF6VscwzDpzOOGhjifQwo_QaxmXw8j4ElJFiGc"


@pytest.fixture
def json_4d(džejsn_4d, posnetek):
    posnetek.api_info = posnetek.pridobi_json(džejsn_4d)
    return posnetek


def test_json_jwt_4d(json_4d, jwt_4d):
    posnetek = json_4d
    posnetek.jwt = posnetek.json_jwt()
    assert posnetek.jwt == jwt_4d


def test_json_povezava_4d(džejsn_api_4d, povezava_do_posnetka_4d, posnetek):
    assert posnetek.json_povezava(
        posnetek.pridobi_json(džejsn_api_4d)) == povezava_do_posnetka_4d


# 365 #######################################################################


@pytest.fixture
def džejsn_365():
    """
    174841952.json
    """
    return r'{"response":{"title":"Sofia Goggia še vedno upa na nastop na olimpijskih igrah ","showName":"Šport","parents":[174841953],"jwt":"EIMCDk5f79eTO4XIN-Ry2fm5-lsbPQPSMy7GfeVCNXk","duration":27,"broadcast":{"genreIds":[160,16050,1605030,160503050],"genre":["ŠPORTNE VSEBINE","PRENOSI IN POSNETKI ZIMSKIH ŠPORTOV","Superveleslalom","Pokali v superveleslalomu"],"idec":"P-1043210-003-2022-023"},"social":{"twitter":"https://twitter.com/tvslosport","email":"gregor.peternel@rtvslo.si"},"broadcastDates":["2022-01-23 22:01:30"],"linkedShows":[],"thumbnails":[{"thumbnail-1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2.jpg","author":null}],"thumbnail_sec":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2.jpg","thumbnails_sec":[{"thumbnail-1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2.jpg","author":null}],"source":"SLO1","geoblocked":1,"clip":1,"status":1,"id":174841952,"recordingDate":"2022-01-23 22:10:47","broadcastDate":"2022-01-23 22:01:30","showId":"494","expirationDate":"3001-01-01 00:00:00","payTv":[],"showDescription":"Pregled športnih dogodkov v dnevnoinformativnih oddajah, kjer se boste seznanili z najnovejšimi rezultati in si ogledali prispevke z aktualnih športnih dogodkov.","showThumbnail":"https://img.rtvcdn.si/_up/ava/ava_misc/show_logos/494/sport_1.jpg","publishDate":"2022-01-23 22:01:57","mediaType":"video","showTypeId":35,"images":{"orig":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2.jpg","fp1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2_fp1.jpg","fp2":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2_fp2.jpg","fp3":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2_fp3.jpg","thumb":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2_thumb.jpg","show":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2_show.jpg","wide1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2_wide1.jpg","wide2":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2022/01/23/2022-01-23-100855-SLO1_part2_wide2.jpg"},"length_min":1,"length_h":27,"length":"00:00:27","date":"23.01.2022","date_slo":"23. 1. 2022","stub":"sport","link":"https://4d.rtvslo.si/arhiv/sport/174841952","showLink":"https://4d.rtvslo.si/oddaja/sport/494","showLinkBySource":"https://www.rtvslo.si/tv/oddaja/sport/494","canonical":{"domain":"https://365.rtvslo.si","path":"/arhiv/sport/174841952"},"show_stats":0,"user_ip":"93.103.250.36","user_id":false,"broadcastDisc":0}}'


@pytest.fixture
def džejsn_api_365():
    return r'{"response":{"mediaFiles_sl":[],"mediaFiles":[{"mediaType":"MP4","bitrate":1800000,"height":720,"id":175220516,"width":1280,"filesize":7478662,"streams":{"hls_sec":"https://vodstr.rtvslo.si/encrypted11/_definst_/2022/01/23/Sofia_Goggia_e_vedno_upa_na_nastop_na_olimpijskih_igrah_2022-01-23-100855-SLO1.mp4/playlist.m3u8?keylockhash=Hc3G77Udti1OP94LdvB6ddzK0rfiPU6_AcV6-mZ3dC8","hls":"http://vodstr.rtvslo.si/encrypted11/_definst_/2022/01/23/Sofia_Goggia_e_vedno_upa_na_nastop_na_olimpijskih_igrah_2022-01-23-100855-SLO1.mp4/playlist.m3u8?keylockhash=Hc3G77Udti1OP94LdvB6ddzK0rfiPU6_AcV6-mZ3dC8"}},{"streams":{"hls":"http://vodstr.rtvslo.si/encrypted11/_definst_/2022/01/23/Sofia_Goggia_e_vedno_upa_na_nastop_na_olimpijskih_igrah_2022-01-23-100855-SLO1_1.mp4/playlist.m3u8?keylockhash=aNP-wFEQszYQQh43yFwCTCzkR_prAQO586CWXxCIX6k","hls_sec":"https://vodstr.rtvslo.si/encrypted11/_definst_/2022/01/23/Sofia_Goggia_e_vedno_upa_na_nastop_na_olimpijskih_igrah_2022-01-23-100855-SLO1_1.mp4/playlist.m3u8?keylockhash=aNP-wFEQszYQQh43yFwCTCzkR_prAQO586CWXxCIX6k"},"filesize":3215795,"height":360,"width":640,"id":175220517,"mediaType":"MP4","bitrate":700000}],"addaptiveMedia":{"hls":"http://vodstr.rtvslo.si/encrypted11/_definst_/2022/01/23/174841952.smil/playlist.m3u8?keylockhash=T0DrTpPfzmFeH0vPnkOzIbA8M6738IBxAIyY0346e2E","hls_sec":"https://vodstr.rtvslo.si/encrypted11/_definst_/2022/01/23/174841952.smil/playlist.m3u8?keylockhash=T0DrTpPfzmFeH0vPnkOzIbA8M6738IBxAIyY0346e2E"}}}'


@pytest.fixture
def povezava_do_posnetka_365():
    """
    hls_sec
    ostale: hls, hls-360. hls_sec-360
    """
    return r'http://vodstr.rtvslo.si/encrypted11/_definst_/2022/01/23/Sofia_Goggia_e_vedno_upa_na_nastop_na_olimpijskih_igrah_2022-01-23-100855-SLO1.mp4/playlist.m3u8?keylockhash=Hc3G77Udti1OP94LdvB6ddzK0rfiPU6_AcV6-mZ3dC8'


@pytest.fixture
def jwt_365():
    return "EIMCDk5f79eTO4XIN-Ry2fm5-lsbPQPSMy7GfeVCNXk"


@pytest.fixture
def json_365(džejsn_365, posnetek):
    posnetek.api_info = posnetek.pridobi_json(džejsn_365)
    return posnetek


def test_json_jwt_365(json_365, jwt_365):
    posnetek = json_365
    posnetek.jwt = posnetek.json_jwt()
    assert posnetek.jwt == jwt_365


def test_json_povezava_365(džejsn_api_365, povezava_do_posnetka_365, posnetek):
    assert posnetek.json_povezava(
        posnetek.pridobi_json(džejsn_api_365)) == povezava_do_posnetka_365

# ars ########################################################################


@pytest.fixture
def džejsn_ars():
    """
    174831008.json
    """
    return r'{"response":{"publishDate":"2021-12-14 14:35:00","showDescription":"Oder, oddaja o sočasnem gledališču, želi podrobno in čim bolj celostno spremljati in predstavljati trenutno domače gledališko dogajanje. Prav tako izpostavlja tudi pomembnejša mednarodna gledališka gibanja ter gostovanja tujih gledaliških skupin ali umetnikov pri nas. Ustvarjanje oddaje je aktualno in raziskovalno. ODER se srečuje s produkcijo slovenskih institucionalnih gledaliških hiš, neodvisne scene, plesnim gledališčem, opero ter mejnimi uprizoritvenimi praksami. Vključuje pregled sočasnih premier, pogovore z ustvarjalci, pregled festivalskega dogajanja in napoved pomembnejših prihodnjih dogodkov. Pogledamo tudi, kje gostujejo domači gledališčniki.","showThumbnail":"https://img.rtvcdn.si/_up/ava/ava_misc/show_logos/15104167/podcast_naslovice_1280x720pxoder.jpg","id":174831008,"payTv":[],"broadcastDate":"2021-12-14 14:05:00","social":{"fbPage":"https://ars.rtvslo.si/oder/","webPage":"https://ars.rtvslo.si/oder/"},"showName":"Oder","jwt":"NYQC77_Qad6riH-IC9p3wz5OOE7mXKPoHeBj2ob2ASI","showId":"15104167","showTypeId":30,"linkedShows":[],"expirationDate":"3001-01-01 00:00:00","broadcastDates":["2021-12-14 14:05:00"],"thumbnails_sec":[{"author":"Petra Tanko","thumbnail-1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147.jpg"}],"title":"Janez Pipan o Hlapcih, ponovitev","podcast":1,"podcastLink":"http://podcast.rtvslo.si/oder.xml","description":"Preteklo soboto so minila 103 leta od smrti Ivana Cankarja. Ob tej priložnosti ne bo odveč še enkrat poslušati pogovor z Janezom Pipanom, ki ga je v sklopu simpozija Stoletje Hlapcev v prostorih Slovenskega gledališkega inštituta vodila Ana Perne. Pipanovi Hlapci so na odru ljubljanske Drame zaživeli konec septembra 2017. V vlogi Jermana je nastopil Marko Mandić, župnika pa je odigral Jernej Šugman. Spominu na gledališkega genija in velikana Jerneja Šugmana, ob četrti obletnici prezgodnje smrti, posvečamo današnjo oddajo. \n\n\nna fotografiji: Marko Mandić in Jernej Šugman v Hlapcih, SNG Drama Ljubljana, sezona 2017/18, foto: Peter Uhan","duration":1987,"broadcast":{"author":"Petra Tanko","idec":"5465118","genreIds":[],"genre":[]},"thumbnails":[{"author":"Petra Tanko","thumbnail-1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147.jpg"}],"recordingDate":"2021-12-14 12:51:21","source":"ARS","thumbnail_sec":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147.jpg","mediaType":"audio","images":{"orig":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147.jpg","fp1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147_fp1.jpg","fp2":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147_fp2.jpg","fp3":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147_fp3.jpg","thumb":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147_thumb.jpg","show":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147_show.jpg","wide1":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147_wide1.jpg","wide2":"https://img.rtvcdn.si/_up/ava/ava_archive11/Content/2021/12/14/ra_slo_5465147_wide2.jpg"},"length_min":33,"length_h":"33:07","length":"00:33:07","date":"14.12.2021","date_slo":"14. 12. 2021","stub":"oder","link":"https://4d.rtvslo.si/arhiv/oder/174831008","showLink":"https://4d.rtvslo.si/oddaja/oder/15104167","showLinkBySource":"https://www.rtvslo.si/radio/oddaja/oder/15104167","canonical":{"domain":"https://365.rtvslo.si","path":"/arhiv/oder/174831008"},"show_stats":0,"user_ip":"93.103.250.36","user_id":false,"broadcastDisc":0}}'


@pytest.fixture
def džejsn_api_ars():
    return r'{"response":{"mediaFiles_sl":[],"mediaFiles":[{"streams":{"https":"https://progressive.rtvslo.si/ava_archive11/2021/12/14/JanezPiRA_SLO_5465118.mp3?keylockhash=x0ogRkrCwGxdjrjauCaODZXzZDefZnho6nH53tVcXsY"},"filesize":31797120,"width":0,"id":175203698,"height":0,"bitrate":128000,"mediaType":"MP3"}]}}'


@pytest.fixture
def povezava_do_posnetka_ars():
    """
    http
    ostale: /
    """
    return r'https://progressive.rtvslo.si/ava_archive11/2021/12/14/JanezPiRA_SLO_5465118.mp3?keylockhash=x0ogRkrCwGxdjrjauCaODZXzZDefZnho6nH53tVcXsY'


@pytest.fixture
def jwt_ars():
    return "NYQC77_Qad6riH-IC9p3wz5OOE7mXKPoHeBj2ob2ASI"


@pytest.fixture
def json_ars(džejsn_ars, posnetek):
    posnetek.api_info = posnetek.pridobi_json(džejsn_ars)
    return posnetek


def test_json_jwt_ars(json_ars, jwt_ars):
    posnetek = json_ars
    posnetek.jwt = posnetek.json_jwt()
    assert posnetek.jwt == jwt_ars


def test_json_povezava_ars(džejsn_api_ars, povezava_do_posnetka_ars, posnetek):
    assert posnetek.json_povezava(
        posnetek.pridobi_json(džejsn_api_ars)) == povezava_do_posnetka_ars


# @pytest.fixture
# def nastavitve():
#     return rtvslo.nastavitve.naloži_nastavitve()

# @pytest.fixture
# def seznam_datotek():
#     path = pathlib.Path(__file__).parent / "../data/json"
#     return list(path.iterdir())


# def jsoni_z_diska():
#     path = pathlib.Path(__file__).parent / "../data/json"
#     datoteke = list(path.iterdir())
#     for i in datoteke:
#         with i.open() as datoteka:
#             yield datoteka.readlines()

# @pytest.mark.parametrize("jsoni_z_diska", jsoni_z_diska)
# def test_json(jsoni_z_diska):
#     for datoteka in jsoni_z_diska:
#         posnetek = rtvslo.rtv.Posnetek("")
#         posnetek.api_info = json.loads(datoteka)["response"]
#         print(posnetek.api_info["jwt"])
# ----------------------------------------------------------------------------
