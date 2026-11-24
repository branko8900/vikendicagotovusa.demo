# -*- coding: utf-8 -*-
"""All page text, Serbian (main) and English.  Lines marked  # DEMO  are sample values to confirm with the owners."""

IG = "https://www.instagram.com/vikendicaa_/"
MAPS = "https://maps.app.goo.gl/WquhpZkN9bn4VkwT8"
PHONE = "+381 64 000 0000"      # DEMO
PHONE_E164 = "381640000000"     # DEMO
POST = {  # the owners' Instagram posts each list row opens
    "in": "https://www.instagram.com/p/DNTAkcjKSZh/",
    "out": "https://www.instagram.com/p/DaZ0OpwiNXz/",
    "winter": "https://www.instagram.com/p/DEqVHXKKKAy/",
    "party": "https://www.instagram.com/p/DNNyTt2qeeW/",
}

SR = dict(
    lang="sr-Latn", root="", other="en/", other_label="English", other_short="EN", other_hreflang="en",
    title="Vikendica Gotovuša — drvena kuća sa bazenom na Šar planini",
    desc="Drvena vikendica za 7 gostiju u Gotovuši, na Šar planini. Bazen, kamin, roštilj i čist planinski vazduh.",
    og_locale="sr_RS",
    skip="Preskoči na sadržaj",
    nav1="Kuća", nav2="Okolina",
    book="Proveri termin",
    menu_open="Otvori meni", menu_close="Zatvori meni", close="Zatvori", to_top="na vrh",

    hero_title="Šar planina", hero_k="1",
    hero_sr="Vikendica Gotovuša na Šar planini",
    tagline="Malo mesto,|veliki odmor",
    hero_alt="Drvena kuća sa okruglim bazenom i ležaljkama, iza nje šumoviti vrhovi Šar planine",
    coll_label="Godišnja doba",
    member_val="5,0",
    member_cap="Ocena gostiju na Google mapama",
    member_alt="Drvena trpezarija sa kamenim kaminom",

    pct_val="750 m", pct_cap="nadmorske visine",
    badge_idx="7",
    badge_t="Do sedam gostiju",
    badge_p="Drvena kuća sa bazenom, kaminom i roštiljem u Gotovuši, na obroncima Šar planine.",
    prev="Prethodni", next="Sledeći", slide="Slajd",

    k_eyebrow="Kuća", k_title="Sve što treba|za odmor",
    rows=[
        ("01", "Unutra", "Drvo, kamen i kamin. Wi‑Fi i Netflix.", "in"),
        ("02", "Dvorište", "Bazen, roštilj, čardak i parking.", "out"),
        ("03", "Zima", "Sneg napolju, vatra u kaminu.", "winter"),
        ("04", "Proslave", "Devojačko, rođendan, Nova godina.", "party"),
    ],
    k_more="Sve fotografije na Instagramu →",

    o_title="Šar planina|na kućnom|pragu",
    o_body="Gotovuša je najveće selo Sirinićke župe i pominje se još od 15. veka. Okolo su pašnjaci, crkve sa starim freskama i šarski sir.",
    dist=[("Štrpce", "10 min"), ("Ski centar Brezovica", "20 min"), ("Skoplje", "1 h 20 min"), ("Priština", "1 h 30 min")],  # DEMO (times)
    o_icon_alt="Šumoviti vrhovi Šar planine pod vedrim nebom",
    t1_name="Jutro u Gotovuši", t1_desc="Magla nad dolinom, pogled iz dvorišta.",
    t1_alt="Dvorište sa bazenom i čardakom, magla nad dolinom",
    t2_name="Kako do nas?", t2_desc="Otvori mapu →",
    t2_alt="Drvena kuća pod oblacima na Šar planini",

    s_eyebrow="U brojkama", s_title="Gotovuša|u brojkama",
    stats=[("750", "m", "Nadmorska visina"), ("7", "", "Gostiju u kući"), ("5,0", "", "Ocena na Google mapama"), ("15.", "", "Vek prvog pomena Gotovuše")],

    g_eyebrow="Gosti", g_title="Rečeno|o Gotovuši",
    quotes=[("Raj na zemlji!!!", "Ivanka N.", "Google mape"),
            ("Savršeno mesto… topla preporuka! Čist planinski vazduh… Divni domaćini…", "Mila M.", "Instagram"),
            ("Мало место за велики одмор…", "Domaćini", "@vikendicaa_")],

    f_eyebrow="Vidimo se", f_big="Spremni|za odmor?",
    f_blurb="Drvena vikendica sa bazenom u Gotovuši, na Šar planini. Leti bazen, zimi kamin i Brezovica.",
    f_place="Gotovuša, opština Štrpce",
    f_col1="Kuća", f_col2="Informacije", f_col3="Pratite nas",
    info=["Prijava od 14:00", "Odjava do 11:00", "Najmanje 2 noći", "od 120 € / noć"],  # DEMO
    f_links=[("Instagram", IG), ("Google mape", MAPS), ("Recenzije", MAPS)],
    copy="© 2026 Vikendica Gotovuša. Demo verzija.",

    m_eyebrow="Proveri termin", m_title="Javite nam|kada dolazite",
    f_name="Ime", f_name_ph="Marko",
    f_from="Dolazak", f_to="Odlazak", f_guests="Gostiju",
    f_msg="Poruka", f_msg_ph="Dolazimo sa dvoje dece i psom…",
    f_wa="Pošalji na WhatsApp", f_viber="Viber",
    m_note="Ili pozovite",
    ok_title="Poruka je spremna",
    menu_links=[("Kuća", "#kuca"), ("Okolina", "#okolina"), ("Gosti", "#gosti"), ("Kontakt", "#kontakt")],
    nf_title="Ova staza ne vodi nigde.", nf_back="Na početnu",

    data=dict(
        lang="sr",
        coll=[
            dict(img="lubenica", brand="Leto", title="Bazen i sunce", cta="Pogledaj kuću", href="#kuca", alt="Kriške lubenice pored bazena"),
            dict(img="zima-noc", brand="Zima", title="Sneg i kamin", cta="Šta ima okolo", href="#okolina", alt="Vikendica u dubokom snegu pod zvezdama"),
            dict(img="devojacko", brand="Proslave", title="Devojačko i rođendani", cta="Proveri termin", href="#book", alt="Luk od balona za devojačko veče u dvorištu"),
        ],
        slides=[
            dict(img="staza", name="Leto", role="Bazen s pogledom na planinu", alt="Kamena staza i kapija, iza kuća, bazen i planina",
                 words=["Bazen,", "Sunce,", "Čist", "Vazduh"]),
            dict(img="zima-kuca", name="Zima", role="Sneg, svetla i kamin", alt="Vikendica noću pod snegom, okićena svetlima",
                 words=["Sneg,", "Kamin,", "Duge", "Noći"]),
            dict(img="sto-zalazak", name="Proslave", role="Sto za sve, zalazak za kraj", alt="Postavljen sto u dvorištu u sumrak, svetla iznad",
                 words=["Roštilj,", "Ekipa,", "Duge", "Večeri"]),
        ],
        send="Pošalji na WhatsApp", sending="Otvaram…",
        err_req="Popunite ovo polje.", err_dates="Odlazak mora biti posle dolaska.",
        thanks="Hvala, {name} — pošaljite poruku i domaćini će vam javiti da li je termin slobodan.",
        there="",
        intro="Zdravo, zanima me slobodan termin u Vikendici Gotovuša.",
        labels=dict(dates="Termin", nights="Noćenja", guests="Broj gostiju", name="Ime", msg="Poruka"),
        nights=["noć", "noći", "noći"],
    ),
)

EN = dict(
    lang="en", root="../", other="", other_label="Srpski", other_short="SR", other_hreflang="sr-Latn",
    title="Vikendica Gotovuša — a wooden cottage with a pool in the Šar Mountains",
    desc="A wooden cottage for 7 guests in Gotovuša, Šar Mountains. Pool, fireplace, barbecue and clean mountain air.",
    og_locale="en_GB",
    skip="Skip to content",
    nav1="House", nav2="Around",
    book="Check dates",
    menu_open="Open menu", menu_close="Close menu", close="Close", to_top="back to top",

    hero_title="Šar Mountains", hero_k="0.8",
    hero_sr="Vikendica Gotovuša in the Šar Mountains",
    tagline="Small place,|big holiday",
    hero_alt="Wooden cottage with a round pool and loungers, forested Šar peaks behind",
    coll_label="Seasons",
    member_val="5.0",
    member_cap="Guest rating on Google Maps",
    member_alt="Log dining nook with a stone fireplace",

    pct_val="750 m", pct_cap="above sea level",
    badge_idx="7",
    badge_t="Up to seven guests",
    badge_p="A wooden house with a pool, fireplace and barbecue in Gotovuša, on the slopes of the Šar Mountains.",
    prev="Previous", next="Next", slide="Slide",

    k_eyebrow="The house", k_title="All you need|to unwind",
    rows=[
        ("01", "Inside", "Wood, stone and a fireplace. Wi‑Fi and Netflix.", "in"),
        ("02", "Garden", "Pool, barbecue, gazebo and parking.", "out"),
        ("03", "Winter", "Snow outside, fire inside.", "winter"),
        ("04", "Celebrations", "Hen parties, birthdays, New Year.", "party"),
    ],
    k_more="All photos on Instagram →",

    o_title="The Šar|Mountains on|the doorstep",
    o_body="Gotovuša is the largest village of the Sirinić župa, recorded since the 15th century. Around it: pastures, churches with old frescoes and Šar cheese.",
    dist=[("Štrpce", "10 min"), ("Brezovica ski centre", "20 min"), ("Skopje", "1 h 20 min"), ("Pristina", "1 h 30 min")],  # DEMO (times)
    o_icon_alt="Forested Šar peaks under a clear sky",
    t1_name="Morning in Gotovuša", t1_desc="Mist over the valley, seen from the garden.",
    t1_alt="Garden with pool and gazebo, mist over the valley",
    t2_name="Getting here", t2_desc="Open the map →",
    t2_alt="Wooden cottage under clouds in the Šar Mountains",

    s_eyebrow="By the numbers", s_title="Gotovuša|in numbers",
    stats=[("750", "m", "Altitude"), ("7", "", "Guests in the house"), ("5.0", "", "Rating on Google Maps"), ("15th", "", "Century of the first record")],

    g_eyebrow="Guests", g_title="What people|say",
    quotes=[("Heaven on earth!!!", "Ivanka N.", "Google Maps · translated"),
            ("A perfect place… warmly recommended! Clean mountain air… Wonderful hosts…", "Mila M.", "Instagram · translated"),
            ("A small place for a big holiday…", "The hosts", "@vikendicaa_ · translated")],

    f_eyebrow="See you", f_big="Ready for|a break?",
    f_blurb="A wooden cottage with a pool in Gotovuša, Šar Mountains. Pool in summer, fireplace and Brezovica in winter.",
    f_place="Gotovuša, Štrpce municipality",
    f_col1="House", f_col2="Details", f_col3="Follow",
    info=["Check-in from 14:00", "Check-out by 11:00", "Minimum 2 nights", "from €120 / night"],  # DEMO
    f_links=[("Instagram", IG), ("Google Maps", MAPS), ("Reviews", MAPS)],
    copy="© 2026 Vikendica Gotovuša. Demo version.",

    m_eyebrow="Check dates", m_title="Tell us|when you're coming",
    f_name="Name", f_name_ph="Alex",
    f_from="Arrival", f_to="Departure", f_guests="Guests",
    f_msg="Message", f_msg_ph="Two adults, two kids and a dog…",
    f_wa="Send via WhatsApp", f_viber="Viber",
    m_note="Or call",
    ok_title="Your message is ready",
    menu_links=[("House", "#kuca"), ("Around", "#okolina"), ("Guests", "#gosti"), ("Contact", "#kontakt")],
    nf_title="This path leads nowhere.", nf_back="To the homepage",

    data=dict(
        lang="en",
        coll=[
            dict(img="lubenica", brand="Summer", title="Pool and sun", cta="See the house", href="#kuca", alt="Watermelon slices by the pool"),
            dict(img="zima-noc", brand="Winter", title="Snow and fire", cta="What's around", href="#okolina", alt="The cottage in deep snow under the stars"),
            dict(img="devojacko", brand="Celebrations", title="Hen parties, birthdays", cta="Check dates", href="#book", alt="Balloon arch for a hen party in the garden"),
        ],
        slides=[
            dict(img="staza", name="Summer", role="A pool with a mountain view", alt="Stone path and gate, the cottage, pool and mountain behind",
                 words=["Pool,", "Sun,", "Clean", "Air"]),
            dict(img="zima-kuca", name="Winter", role="Snow, lights and a fire", alt="The cottage at night under snow, lit with string lights",
                 words=["Snow,", "Fire,", "Quiet", "Nights"]),
            dict(img="sto-zalazak", name="Celebrations", role="One long table, one sunset", alt="A laid table in the garden at dusk, lights above",
                 words=["Grill,", "Friends,", "Long", "Dinners"]),
        ],
        send="Send via WhatsApp", sending="Opening…",
        err_req="Please fill this in.", err_dates="Departure must be after arrival.",
        thanks="Thanks, {name} — send the message and the hosts will tell you if the dates are free.",
        there="",
        intro="Hello, I'd like to check availability at Vikendica Gotovuša.",
        labels=dict(dates="Dates", nights="Nights", guests="Guests", name="Name", msg="Message"),
        nights=["night", "nights", "nights"],
    ),
)
