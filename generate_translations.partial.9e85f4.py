#!/usr/bin/env python3
"""
Generate English translations for spots.json and festivals.json
Style: Atlas Obscura / Tofugu — intellectual, edge, storytelling
"""
import json
import copy

# ─────────────────────────────────────────────
# SPOTS TRANSLATIONS
# ─────────────────────────────────────────────

SPOTS_EN = {
    "spot-001": {
        "name_en": "Tagata Shrine (Phallus Shrine)",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Komaki City",
        "summary_en": "If you've ever wondered whether a 2-meter, 60-kilogram wooden phallus could be the star of a major religious festival, Tagata Shrine has your answer. This unassuming Shinto shrine in Komaki City holds the Hōnen Festival every March — an annual celebration of fertility, bumper harvests, and human reproduction that has drawn BBC crews, CNN cameras, and tens of thousands of visitors who make the pilgrimage specifically to witness Japan's most globally famous bizarre ritual. The festival's centerpiece is a colossal carved phallus mikoshi — the divine portable shrine — that is paraded through the streets to thunderous cheers and delighted disbelief. But even outside festival season, Tagata's grounds are remarkable: votive offerings in every conceivable phallic shape crowd the shrine precincts, donated by supplicants praying for fertility, easy childbirth, and agricultural abundance. The tradition roots back to ancient Japanese folk religion, when the earth's creative power was openly celebrated in forms that later eras might euphemize but never entirely erased. The nearby Ōagata Shrine — dedicated to feminine fertility — sits a short drive away, making this one of Japan's great \"yin and yang\" shrine circuits, completable in a single morning. What reads as provocative to modern eyes was, for centuries, simply the honest language of a people who depended on the land and the continuation of their lineage.",
        "highlights_en": [
            "A 2-meter sacred phallus mikoshi paraded through city streets to an audience of tens of thousands",
            "Shrine grounds packed with votive phallus offerings of every shape and scale — an overwhelming, unforgettable spectacle",
            "Internationally renowned: BBC, CNN and foreign press descend every March, making this Japan's most-covered bizarre festival"
        ]
    },
    "spot-002": {
        "name_en": "Ōagata Shrine (Vulva Shrine)",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Inuyama City",
        "summary_en": "If Tagata Shrine is Japan's yin, Ōagata Shrine is its yang — or rather the reverse: the feminine counterpart in one of the world's most candid pairs of fertility shrines. While Tagata worships the phallus, Ōagata venerates the feminine principle through its spring Hime-no-Miya Festival (also known irreverently as the Ososo Matsuri), held annually on March 15th — the same day and in the same general area as Tagata's Hōnen Festival. The parade's centerpiece is a pink, peach-shaped portable shrine, and visitors are offered pink yōkan sweets shaped in the same unmistakable motif. The double-billing with Tagata on the same date makes this area around Inuyama a uniquely concentrated zone of ancient Japanese sexual symbolism — what scholars call the \"yin-yang twin festival circuit,\" where ancient agrarian fertility worship survives intact into the Instagram age. Inuyama itself is the heartland of the Momotarō (Peach Boy) folk legend, adding mythological layers to the shrine's peach iconography. The grounds are lined with peach-shaped ema votive plaques, and the shrine's famous plum grove reaches full bloom precisely in time for the spring festival. Coming here after Tagata is less of an afterthought and more of a completion — two halves of an ancient cosmological equation.",
        "highlights_en": [
            "A pink, peach-shaped portable shrine paraded by crowds — the feminine answer to Tagata's phallus mikoshi",
            "The ultimate bizarre-festival double-header: both shrines hold their rites on the same day, just 10 minutes apart by car",
            "Grounds filled with peach-shaped ema votive plaques, weaving together Momotarō mythology and ancient fertility symbolism"
        ]
    },
    "spot-003": {
        "name_en": "Goshikien (Five-Color Garden)",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Nisshin City",
        "summary_en": "Somewhere in the forest-covered hills of Nisshin City, Japan's only religious theme park quietly pushes the boundary between Buddhist devotion and folk-art fever dream. Founded in 1934 by a Buddhist organization, Goshikien sprawls across more than 66 hectares of woodland, where roughly 100 life-sized concrete sculptures — the life's work of self-taught sculptor Asano Shōun — stand amid the trees like a frozen congregation. Shōun, who carved religious figures from concrete with a hypnotic intensity that has earned him the nickname \"Japan's Gaudí,\" spent decades recreating scenes from the life of Shinran, the founder of Jōdo Shinshū Buddhism. The results are vivid, bold, and startlingly expressive: monks with eyes that seem to track you, devotees frozen in extremity, facial expressions hovering somewhere between agony, enlightenment, and something much harder to name. Whether Goshikien is sacred art or outsider art or the most spectacular B-kyū spot in Japan is a question that seems beside the point once you're standing in the woods with concrete saints looming over you. Entry is free — which feels impossible given the sheer scale and ambition of the place — making it a rare instance where the most surreal attraction in the prefecture is also the most accessible.",
        "highlights_en": [
            "Nearly 100 oversized concrete religious figures lurking in a dense forest — scale and density that must be experienced in person",
            "One of the three great Asano Shōun sacred sites, alongside Sekigahara WarLand and Momotarō Shrine",
            "Free admission, yet the volume and ambition of the sculptural landscape rivals any paid attraction in the region"
        ]
    },
    "spot-004": {
        "name_en": "Momotarō Shrine (Peach Boy Shrine)",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Inuyama City",
        "summary_en": "Perched above the Kiso River on a sheer cliff face, Momotarō Shrine is dedicated to the Peach Boy — Japan's most beloved folk hero — and it wears that dedication with an absolutely unhinged kind of pride. The approach passes through a torii gate shaped like a giant pink peach, setting the tone for what follows: dozens of concrete sculptures by the legendary Asano Shōun, depicting demons, ogres, hags, and the hero himself in poses that range from triumphant to deeply unsettling. Shōun's figures have a particular genius for capturing the grotesque — the veins bulging on a demon's arm, the manic glee of a conquering warrior, the sorrow of a defeated enemy. Inside the modest treasure hall, an eccentric collection of local donations and strange curios completes the experience in ways that no museum curator would sanction. The shrine sits at the confluence of Momotarō mythology and Asano Shōun's concrete universe, making it a keystone of what local enthusiasts call the \"Asano Ginga\" (Asano Galaxy) — the cluster of Shōun works concentrated in this corner of Aichi. Below the shrine, the Kiso River flows in a vista of genuine beauty, which makes the concrete demons above it all the more disorienting.",
        "highlights_en": [
            "A pink giant-peach torii gate — the only one of its kind on Earth — announces an experience like nothing else",
            "Asano Shōun's concrete ogres and demons, with anatomically exaggerated veins and haunting expressions that blur the line between folk art and nightmare",
            "The treasure hall's bizarre donated collection is wildly off-script from any recognizable museum logic — the chaos is the exhibit"
        ]
    },
    "spot-005": {
        "name_en": "Yoro Tenmei Aichi (Reversible Destiny Lofts)",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Yōrō Town, Yōrō District",
        "summary_en": "In 1994, world-renowned artist Arakawa Shūsaku and poet Madeline Gins completed what they believed would be a physical argument against death — an 18,000-square-meter landscape specifically engineered to disorient the human body into a state of radical aliveness. What they actually created is a place where nearly everyone falls down. The Yoro Tenmei Aichi (\"Site of Reversible Destiny\") is a vast oval depression containing five island-shaped mounds modeled after the Japanese archipelago, crossed by 148 pathways that slope, lurch, and tilt in directions that resist the brain's predictions. The ground is never flat. The walls lean. The staircases make no promises. Visitors with full physical mobility routinely find themselves clutching each other for balance, laughing and swearing in equal measure, arriving at a paradoxical clarity about what it means to inhabit a body. This is the work's genius: its stated purpose is to make you immortal through destabilization; its actual method is to make you concentrate so hard on not falling that everything else falls away. As both a landmark of contemporary art and an extreme B-kyū experience, it has no peer.",
        "highlights_en": [
            "A landscape where nearly every surface is sloped, warped, or otherwise hostile to upright walking — falling is not a malfunction, it's the point",
            "The philosophical provocation is genuine: Arakawa and Gins believed that confusing the body's habits could delay aging and death",
            "Accessible to everyone, yet no one gets through unscathed — a rare equal-opportunity physical experience"
        ]
    },
    "spot-006": {
        "name_en": "Sekigahara WarLand",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Sekigahara Town, Fuwa District",
        "summary_en": "In the year 1600, on a misty plain in what is now Gifu Prefecture, the Battle of Sekigahara decided the future of Japan — 160,000 soldiers clashing in the decisive conflict that brought the Tokugawa shogunate to power. Today, that same plain hosts something far stranger than history: 240-plus life-sized concrete warriors, painted in vivid folk-art colors by the singular Asano Shōun, frozen in perpetual combat across a sprawling outdoor theme park. WarLand occupies its own peculiar niche — part history lesson, part outsider art installation, part low-budget theme park — and it refuses to commit fully to any of those categories. The warrior figures are hyperrealistic in pose and garish in color, arranged to recreate specific tactical moments of the battle with educational placards that sit incongruously beside Shōun's fever-dream aesthetic. Come at night, when the figures are lit from below: the darkness dissolves the educational context entirely and leaves you with 240 glowing samurai materializing from shadow, an image that belongs more to a waking nightmare than a history exhibit. This is one of three great Asano Shōun pilgrimage sites in the region — the others are Goshikien and Momotarō Shrine — and for sheer scale, WarLand is his magnum opus.",
        "highlights_en": [
            "240-plus life-sized concrete samurai standing across an open battlefield — a scale that photographs cannot prepare you for",
            "Night illumination transforms the educational park into something genuinely eerie: glowing warriors emerging from darkness",
            "The site occupies the actual historical battlefield of 1600, layering absurdist folk art over one of Japan's most consequential real events"
        ]
    },
    "spot-007": {
        "name_en": "Chinpin Center (Curiosity Castle)",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Yōrō Town, Yōrō District",
        "summary_en": "Somewhere along the road near Yoro, a castle suddenly appears — not a real castle, but a building topped by two golden shachihoko (mythical carp-tigers) in the style of Nagoya Castle's famous roof ornaments, encasing a rambling labyrinth of antiques, folk crafts, military paraphernalia, ceramics, old furniture, and the kind of objects that defy classification. The Chinpin Center, colloquially known as \"Chinpin Castle,\" operates on the belief that every object has intrinsic worth and that the right buyer is somewhere in the world, given sufficient accumulation. The interior is an organized chaos that rewards slow exploration: old woodblock prints lean against lacquered tansu chests, rusted farm implements hang above porcelain tea sets, and the proprietor — usually present — dispenses commentary that blurs the line between sales pitch and performance art. Its location adjacent to the Yoro Tenmei Aichi (Reversible Destiny Lofts) makes it the perfect cooldown stop after a morning of falling over in the name of art. Visiting both in sequence is the de facto \"Yoro oddity circuit\" and one of the most absurdly satisfying half-days in the Tōkai region.",
        "highlights_en": [
            "The roadside appearance of a golden-shachihoko castle has a visual impact that no description can blunt",
            "The interior is a genuine labyrinth of antiques, folk artifacts, and unclassifiable objects — hours pass unnoticed",
            "Perfect pairing with the Yoro Tenmei Aichi next door: combine both for a single \"Yoro Oddity Tour\""
        ]
    },
    "spot-008": {
        "name_en": "Atami Hihoukan (Secret Treasure Museum)",
        "prefecture_en": "Shizuoka Prefecture",
        "city_en": "Atami City",
        "summary_en": "Japan's hihoukan — \"secret treasure museums\" — were a genre of adult entertainment attraction unique to the Shōwa era: theme parks of erotic folk art, carved automata, and painted dioramas that occupied a peculiar space between cultural education and carnivalesque titillation. At their peak in the 1970s and 80s, hihoukan dotted the resort coastlines of Japan, offering honeymooning couples a transgressive supplement to their hot spring holidays. Most are gone now, their campy maximalism incompatible with the sanitized aesthetics of modern tourism. The Atami Hihoukan survives as the last major heir to this tradition, and as a result it has become something more than entertainment: it is a living fossil of an entire social attitude, a preservation of an era when Japanese resort culture was uninhibited in ways that contemporary travel can barely imagine. The extra layer of absurdity — that reaching it requires a ropeway ride up a hillside — was clearly an intentional piece of theatrical staging, ensuring that the ascent itself becomes part of the spectacle. For the cultural historian, the Japan nostalgia obsessive, or simply the traveler who wants to see something genuinely impossible to find anywhere else on Earth, the Atami Hihoukan rewards the detour.",
        "highlights_en": [
            "The ropeway approach is deliberate theatrical architecture — inconvenience as showmanship",
            "A living museum of Shōwa-era adult entertainment culture that no longer exists anywhere else at this scale",
            "For the right visitor, this is not titillation but archaeology: Japan in the 1970s, preserved in amber"
        ]
    },
    "spot-009": {
        "name_en": "Ayashii Shōnen Shōjo Hakubutsukan (Museum of Strange Boys and Girls)",
        "prefecture_en": "Shizuoka Prefecture",
        "city_en": "Itō City",
        "summary_en": "The sign outside features a giant penguin in a top hat. This should tell you everything. Inside, the Museum of Strange Boys and Girls presents itself as a children's attraction — and it is, sort of — while delivering an experience that obliterates most adults with waves of involuntary nostalgia. The collection is a dense, delirious archive of Shōwa-era toys, tin robots, candy-shop décor, penny arcade machines, department-store mascots, and the kind of mass-produced objects from the 1950s through 70s that once felt ordinary and now feel like artifacts of a vanished civilization. Display density is the operative principle: objects are packed floor to ceiling, shelf to shelf, in a visual accumulation that overwhelms the eye and floods the memory of anyone old enough to remember what dagashi-ya (penny candy shops) smelled like. Children visiting today find it genuinely weird in the best possible sense; adults who grew up in Japan find it genuinely devastating in the best possible sense. The adjacent Maboroshi Hakurankai (Phantom World Exposition) operates in a similar register, and doing both in sequence constitutes an unofficial pilgrimage through Japan's retro-culture paradise in the hills above Izu.",
        "highlights_en": [
            "The giant tuxedo penguin at the entrance is not ironic — it's the museum's whole aesthetic in a single image",
            "An impossible density of Shōwa-era objects that creates a physical sensation of time travel",
            "The nearby Maboroshi Hakurankai makes for an unmissable back-to-back retro afternoon"
        ]
    },
    "spot-010": {
        "name_en": "Oku-Maya Amusement Park Ruins",
        "prefecture_en": "Hyōgo Prefecture",
        "city_en": "Kōbe City, Nada Ward",
        "summary_en": "At the summit of Mount Maya, 702 meters above Kōbe, there was once a mountain amusement park: roller coasters, an outdoor amphitheater, an ice skating rink, all suspended above the city in a fantasy of elevated leisure. The park is long gone, closed and reclaimed by the mountain's vegetation, but the traces remain — concrete foundations, rusting infrastructure, the ghost of a roller coaster track faintly visible through the undergrowth — giving the site the quality of a discovery rather than a destination. The nearby Kyū Maya Kankō Hotel (\"Mayakan\") compounds the atmosphere: a 1929 Art Deco ruin that has achieved the rare status of being both a registered cultural property and a genuine abandoned building simultaneously. Together, the park ruins and Mayakan constitute what urban explorers call a \"Maya mountain ruin circuit\" — a journey through the life cycle of mid-century Japanese mountain tourism, from its Art Deco aspirations to its overgrown aftermath. The view from the summit, meanwhile, remains as spectacular as it ever was: the entire Kansai plain spread below, Ōsaka Bay gleaming to the west.",
        "highlights_en": [
            "The gap between the fantasy of a mountaintop amusement park and its current state of silent decay is one of the most atmospheric experiences in the Kansai region",
            "The roller coaster's rusting skeleton is still faintly visible on the hillside — a ghost of kinetic energy frozen in vegetation",
            "Combine with Mayakan (the Kyū Maya Kankō Hotel) for the complete Mount Maya abandoned-luxury circuit"
        ]
    },
    "spot-011": {
        "name_en": "Tower of the Sun (Interior)",
        "prefecture_en": "Ōsaka Prefecture",
        "city_en": "Suita City",
        "summary_en": "Okamoto Tarō's 70-meter concrete colossus has presided over the former grounds of Expo '70 since it was erected for the 1970 World Exposition — too strange to demolish, too iconic to ignore, it simply stood there for 48 years with its sealed interior unexplored, its internal world a rumor. In 2018, that interior was finally opened to the public, revealing what may be the most extraordinary thing a famous exterior has ever been hiding. Inside the Tower of the Sun, a structure called the \"Tree of Life\" spirals upward through the tower's core: a 45-meter sculptural column bearing 183 models of creatures representing the evolution of life on Earth, from primordial single-celled organisms to modern primates. The models escalate in complexity and in strangeness, reaching the tower's crown in a tumult of primates and proto-humans, with Okamoto's characteristic aesthetic — vivid, raw, confrontational — applied at biological scale. An additional exhibit reconstructs the \"Face of the Earth\" (the Black Sun), a fourth face that was once displayed on the tower's base before being lost; its restoration adds a mythological dimension to an already overwhelming experience. Visiting the inside after knowing only the outside feels like discovering that a familiar landmark has been secretly a living organism all along.",
        "highlights_en": [
            "183 life-size evolutionary creature models spiraling up the tower's interior — a density and strangeness that redefines the word \"installation\"",
            "The reconstructed \"Black Sun\" — the lost fourth face of the tower — adds a mythological layer that the exterior never hinted at",
            "For 48 years this interior was sealed: the sense of finally accessing a forbidden space has not diminished"
        ]
    },
    "spot-012": {
        "name_en": "Namba Yasaka Shrine (Lion Head Shrine)",
        "prefecture_en": "Ōsaka Prefecture",
        "city_en": "Ōsaka City, Naniwa Ward",
        "summary_en": "Somewhere in the dense residential and commercial tangle of Namba, a 12-meter demon's head erupts from the ground behind an ordinary shrine wall. The獅子殿 (Shishiden) — the Lion Stage — is a performance hall built in the form of a massive oni-lion face, with gaping jaws as the entrance and eyes that (during special events) issue fire. It is the only structure of its kind in Japan. What makes Namba Yasaka truly odd is not just the building but its context: this is a functioning neighborhood shrine, visited by local residents for perfectly ordinary reasons — traffic safety, academic success, business prosperity — who apparently see nothing unusual about worshipping beside a giant fire-breathing demon head. The shrine is not marketed as a tourist attraction, does not operate like one, and seems genuinely indifferent to the bewilderment it causes in visitors arriving from abroad. This quality of aggressive normalcy — the demon head as unremarkable background detail of daily neighborhood life — is the most Ōsaka thing imaginable, and also the most unsettling.",
        "highlights_en": [
            "A 12-meter oni-lion head used as a functioning shrine stage — the only structure of its kind in existence",
            "Eyes and nose that emit actual fire during special events, operated by a shrine that treats this as entirely routine",
            "The complete absence of tourist-facing presentation: this is simply the local shrine, and the demon head is simply its stage"
        ]
    },
    "spot-013": {
        "name_en": "Ikoma Sanjō Amusement Park",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Ikoma City",
        "summary_en": "Opened in 1929, the Ikoma Sanjō Amusement Park holds the distinction of being Japan's oldest surviving mountain amusement park — a category that, it turns out, is more interesting than it sounds. The park sits at 642 meters on the summit of Mount Ikoma, straddling the prefectural border between Ōsaka and Nara, which means that the jurisdictional line between the two prefectures runs directly through the park grounds — a legal peculiarity with no precedent in Japanese theme park history. The rides are vintage Shōwa, the crowds are families with small children, and the atmosphere carries the specific quality of an older Japan still functioning on its own terms, unrevised by the demands of contemporary entertainment design. At night, with Ōsaka's vast grid of lights spread below on one side and Nara's quieter valleys on the other, the park achieves a kind of inadvertent grandeur. The Ikoma Cable Car — itself a historic piece of engineering — delivers you to the summit with a theatrical sense of vertical separation from the world below.",
        "highlights_en": [
            "Japan's oldest surviving mountain amusement park — a title with genuine historical weight",
            "The Ōsaka/Nara prefectural border passes through the park itself — the only amusement park in Japan to contain an inter-prefecture boundary",
            "Shōwa-era rides still operating against a backdrop of two-prefecture night views: a temporal dislocation unlike any other"
        ]
    },
    "spot-014": {
        "name_en": "Former Nara Prison (Meiji-Era Heritage Hotel)",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Nara City",
        "summary_en": "Built in 1908 as part of a Meiji-era prison modernization initiative, the Former Nara Prison is one of five remaining \"Meiji Five Great Prisons\" — European-influenced, radially designed correctional facilities whose architecture owes more to Bentham's panopticon than to anything in Japanese building tradition. The prison's red-brick Neo-Gothic exterior and radial cell block layout are extraordinary in a country where almost nothing from that era survives intact. After serving as a juvenile detention facility until 2017, the building was redeveloped as a combination hotel, museum, and heritage attraction, reopening in 2023. Guests now sleep in former cells converted to hotel rooms; day visitors can walk the original radiating corridors, the chapel, and the exercise yard on guided tours. The combination of proximity to Nara Park's deer and temples (all within walking distance) with the option of actually sleeping inside a 120-year-old prison creates a travel experience that exists nowhere else in Japan.",
        "highlights_en": [
            "You can spend the night in a converted 19th-century prison cell — an experience that remains unique in Japan",
            "The Meiji red-brick architecture and panopticon-style radiating cell blocks are architectural treasures of singular rarity",
            "Day tours through the original cell blocks, chapel, and courtyard are available for non-staying visitors"
        ]
    },
    "spot-015": {
        "name_en": "Shigaraki Giant Tanuki Colony",
        "prefecture_en": "Shiga Prefecture",
        "city_en": "Kōka City, Shigaraki Town",
        "summary_en": "The humble, wide-bellied, sake-jug-holding tanuki (raccoon dog) figurine — a fixture outside every izakaya and sake shop in Japan — was born in Shigaraki. This unassuming town in the Kōka hills of Shiga Prefecture is the origin point of Japan's most ubiquitous ceramic mascot, and it celebrates that fact with the kind of maximalist enthusiasm that only a town with a single defining product can muster. Stepping off the Shigaraki Kōgen Railway (itself a charming piece of rural nostalgia) deposits you in a world comprehensively colonized by raccoon dogs: they line the station platforms, flank the shopping streets, crowd the gallery gardens, and occupy every conceivable surface of the Tanuki Village (Tanuki-mura), the town's main attraction. The figures range from canonical to experimental — some the size of garden ornaments, others as tall as a person, a few in frankly inexplicable colorways. The collective effect of all this pottery-animal accumulation — rows and rows of wide-eyed ceramic creatures smiling in unison — tips from charming into faintly uncanny in a way that is deeply, specifically Japanese.",
        "highlights_en": [
            "From the moment you step off the train, every direction offers a tanuki — a total environmental colonization by one ceramic mascot",
            "The sheer variety at Tanuki-mura, from classical figures to aggressively avant-garde interpretations, creates a genuinely chaotic visual experience",
            "You can throw a Shigaraki ceramic tanuki on a pottery wheel and carry home the weirdest possible souvenir"
        ]
    },
    "spot-016": {
        "name_en": "Hananoiwaya Shrine (The Flower Rock Shrine)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Kumano City",
        "summary_en": "There is no hall. There are no carved wooden columns, no gilded altar fittings, no roof. At Hananoiwaya, the shrine is a 45-meter cliff face of raw granite, and that is everything. This is considered one of the oldest places of worship in Japan — the Chronicles of Japan (Nihon Shoki) place its founding at the very dawn of the Japanese state — and its utter simplicity suggests something about what Shinto looked like before the religion adopted the architectural language of imported Buddhism. The cliff is said to be the burial place of Izanami, the goddess who died giving birth to the fire deity Kagatsuchi, whose tomb you can walk along, touching what mythology tells you is the resting place of the creator of Japan. Twice a year, in February and October, the Otsunanukake ceremony strings enormous ropes of braided cloth between the cliff face and a ceremonial platform, in a rite that has continued unchanged for at least two thousand years. The site was designated part of the Kumano Kodō UNESCO World Heritage route in 2004 — a recognition that felt, to regular visitors, like merely official confirmation of something they already knew.",
        "highlights_en": [
            "A 45-meter cliff is the entire shrine — no building, no hall, just raw rock as deity, unchanged for over two millennia",
            "The mythological weight of the location: this cliff is said to be the actual grave of Izanami, mother of the Japanese islands",
            "The biannual Otsunanukake rope-stringing ceremony is one of the oldest continually performed rituals in Japan"
        ]
    },
    "spot-017": {
        "name_en": "Futami Okitama Shrine and Meoto Iwa (Wedded Rocks)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Ise City",
        "summary_en": "Two rocks in the sea, connected by a shimenawa sacred rope — this is the essential image of Futami, and it has been the essential image for at least a thousand years of uninterrupted religious significance. The larger rock stands nine meters, the smaller four; the rope connecting them (changed three times a year in elaborate ceremony) links them as husband and wife, and through their union, they frame a view of the submerged sacred stone of Okitama and the distant profile of Mount Fuji at sunrise, at least on exceptionally clear mornings. The rocks serve as a kind of natural torii gate for the offshore sacred stone, which sits 700 meters out in Ise Bay. Pilgrims visiting the Grand Shrine of Ise (Jingū) traditionally stopped at Futami to purify themselves in the sea beforehand — a practice that has declined but not disappeared. The shrine precincts are dense with frog sculptures (the frog, or kaeru, is a homophone for \"return\" — returning safely from a journey), donated by pilgrims over centuries until the accumulation has become a peculiar frog-filled landscape in its own right. At the summer solstice, the sun rises precisely between the two rocks — an alignment that cannot be accidental and implies a knowledge of celestial geometry in ancient coastal Japan that continues to astonish.",
        "highlights_en": [
            "Two rocks joined by a sacred rope serve as a living torii gate to a submerged shrine stone 700 meters offshore — Shinto cosmology made physical",
            "The shrine grounds are carpeted in centuries of donated frog sculptures — a uniquely accumulative folk devotion that has created its own strange landscape",
            "At the summer solstice, the sun rises exactly between the two rocks: evidence of ancient astronomical precision that still defies easy explanation"
        ]
    },
    "spot-018": {
        "name_en": "Former Meki Tunnel (Onigami Tunnel)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Taki Town, Taki District",
        "summary_en": "The name alone — Meki, written with the characters for \"female demon\" — seems to have been designed to ensure this tunnel would never entirely shed its reputation. Mie Prefecture's most notorious haunted site, the old Meki Tunnel sits in a fold of the Watarai mountains southeast of Matsusaka, its stone entrance draped in moss, its interior cold even in summer. The legends around it are specific in the way that the best ghost stories always are: a woman's figure that climbs into the back seat of cars; an engine that dies without explanation at the tunnel's midpoint; a chill that intensifies as you approach the old stone portal. The tunnel is currently closed to entry, and this is presented as a genuine warning rather than a formality. Whether you believe in the paranormal or not, the physical fact of the location — a moss-covered stone tunnel at the end of a narrow mountain road, surrounded by an abandoned hamlet, carrying a name that means \"female demon\" — is an exceptionally well-composed piece of environmental atmosphere.",
        "highlights_en": [
            "The place name \"Meki\" — literally \"Female Demon\" — is not a marketing decision but an ancient toponym that has haunted locals for centuries",
            "A moss-covered stone tunnel entrance with a quality of dread that does not require supernatural belief to appreciate",
            "Consistently ranked as Mie Prefecture's most famous haunted site — the institutional benchmark against which all local ghost stories are measured"
        ]
    },
    "spot-019": {
        "name_en": "Former Nagano Tunnel (Long Peak Pass)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Tsu City / Iga City border",
        "summary_en": "The Nagano Pass connecting Tsu and Iga cities is unusual in that it contains tunnels from three different eras — Meiji, Taishō, and Shōwa — each bored through the same mountain range decades apart, each now in a different state of abandonment, their combined presence creating a kind of geological layer cake of early modern Japanese infrastructure. The oldest tunnels are largely consumed by vegetation. The old road that connected them is now impassable for most of its length, designated a废道 (废道 — abandoned road) and left to the mountain. Reported apparitions reflect this layered history: a figure in workman's overalls (from the construction era?), a headless motorcyclist (from the postwar highway era?), multiple presences whose apparent vintage spans the tunnel complex's full operational period. For those interested in either the paranormal or the industrial archaeology of early modern Japan, the Nagano Pass offers an exceptionally atmospheric site within easy reach of Kameyama.",
        "highlights_en": [
            "Three tunnels from three separate eras sharing a single mountain pass — a uniquely stratified piece of modern Japanese infrastructure history",
            "The reported ghosts reflect the site's layered history: apparitions from multiple decades occupying the same abandoned road",
            "One of Mie's most accessible major haunted sites, reachable within 30 minutes from Kameyama"
        ]
    },
    "spot-020": {
        "name_en": "Yunoyama Onsen Abandoned Hotel District",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Kōmono Town, Mie District",
        "summary_en": "Yunoyama Onsen has been a hot spring resort since the Edo period — nearly 400 years of travelers soaking in the volcanic waters of the Suzuka mountains. At its postwar peak, the resort town was a Shōwa-era paradise of ryokan inns and resort hotels catering to factory workers and families from the surrounding industrial cities. Then the economics shifted, and the inns began to close. The Sugiya Ryokan, one of the oldest inns in the entire onsen region, is among the structures left behind — its distinctive architecture now slowly surrendering to the mountain. What was once a destination for celebration (anniversaries, honeymoons, company retreats) is now a photogenic ruin that draws a different kind of visitor: urban explorers, horror enthusiasts, and anyone drawn to the specifically Japanese phenomenon of the abandoned resort, which carries an emotional charge unlike any other kind of ruin. In 2024 and 2025, the Sugiya was officially developed as a horror event venue — a telling commentary on the economic logic of Japanese ghost tourism.",
        "highlights_en": [
            "The abandoned Sugiya Ryokan carries nearly 400 years of resort history in its collapsing walls — an extraordinarily weighted ruin",
            "The official conversion of the ruins to a horror event venue is a fascinating document of contemporary Japanese dark-tourism economics",
            "Just 30 minutes from Kameyama, making it the most accessible major abandoned site in the region"
        ]
    },
    "spot-021": {
        "name_en": "Adashino Nenbutsuji Temple (8,000 Stone Buddhas)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Ukyō Ward",
        "summary_en": "At the far end of the Saga Arashiyama tourist corridor, past the last souvenir shops and the last bamboo grove photo opportunities, Adashino Nenbutsuji sits in the quiet upper reaches of Sagano — a Pure Land Buddhist temple whose grounds are home to approximately 8,000 stone Buddhas and grave markers, packed into the hillside in configurations that approach geological density. The site's origin is grim: in ancient times, this area at the edge of the capital was where the bodies of those who died without family or resources were left to decompose, unburied and unmourned. The priest Kūkai (Kōbō Daishi) is said to have gathered and enshrined the abandoned dead here in the ninth century, beginning a tradition of memorial that has continued ever since. Each August, during the Sentō Kuyō ceremony, the stone figures are illuminated by hundreds of bamboo lanterns — an event of such concentrated otherworldly beauty that visitors regularly describe it as the most visually overwhelming thing they have ever seen. Throughout the year, without special illumination, the sheer accumulated mass of stone figures produces a quality of atmosphere that is entirely its own.",
        "highlights_en": [
            "8,000 stone Buddhas packed into a hillside cemetery create a visual experience for which there is no adequate comparison",
            "The August Sentō Kuyō bamboo lantern ceremony illuminates every stone figure simultaneously — one of the most extraordinary ritual spectacles in Kyōto",
            "Founded as a memorial to the nameless dead: the weight of that original act of compassion still shapes the atmosphere of the entire site"
        ]
    },
    "spot-022": {
        "name_en": "Kubizuka Daimyōjin (Shuten-dōji's Head Mound)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Nishikyō Ward",
        "summary_en": "On the Old Nishikyō Road at the summit of Ōenok坂 Pass, tucked at the end of a narrow lane dark even at noon, a small shrine marks the spot where Japan's most feared oni — Shuten-dōji, the leader of a demonic mountain cult — is said to have been buried after his decapitation by the warrior Minamoto no Yorimitsu in the 10th century. The story goes that even after its owner was killed, Shuten-dōji's severed head flew through the air and bit one final time before finally going still, which suggests the head was buried here as much to contain it as to honor it. The site carries an additional layer of historical resonance: it is traditionally identified as the spot where Akechi Mitsuhide paused in 1582 before marching on Honnō-ji to assassinate Oda Nobunaga, as if the buried demon's energy provided some final reinforcement of his resolve. A convenience store and a shuttered love hotel currently flank the approach — a juxtaposition that feels almost designed.",
        "highlights_en": [
            "The burial site of Japan's most powerful mythological demon — a category of spiritual real estate with almost no competitors",
            "Tradition links this spot to Akechi Mitsuhide's decision to betray Oda Nobunaga in 1582: the demon's mound as a hinge point of Japanese history",
            "The contrast between the site's mythological weight and its mundane contemporary surroundings is one of the most quintessentially Japanese spatial experiences imaginable"
        ]
    },
    "spot-023": {
        "name_en": "Toribeno (Kyōto's Ancient Mortuary Plain)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Higashiyama Ward",
        "summary_en": "The hills east of Kiyomizudera, now among the most visited tourist corridors in Japan, sit atop a zone that served for centuries as one of the capital's principal disposal sites for the dead. The area known as Toribeno — stretching from the base of Higashiyama through to Mount Amidagamine — was a site of sky burial, wind burial, and open exposure of corpses from the Heian Period through the early Edo Period, its landscape described in Japanese literature (the Tale of Genji, among others) as the quintessential entrance to the afterworld. The bones are, in a literal sense, beneath the souvenir shops and the matcha soft serve vendors. The Rokudō Chinkōji Temple on the same street marks what is known as \"the crossroads of the six worlds\" — the junction between the living and the dead — and its annual Rokudō Mairi ceremony in August is an active practice of summoning ancestors' spirits back from the dead for the Obon season. No other tourist destination in Japan carries quite this degree of necromantic subtext.",
        "highlights_en": [
            "Japan's most visited tourist quarter literally stands on what was once the city's primary burial ground — the bones are still there",
            "Rokudō Chinkōji Temple maintains an active portal between the living and the dead, visited by thousands during the annual Obon season",
            "Toribeno appears in The Tale of Genji as the archetypal entrance to the underworld — over a thousand years of literary mortuary geography concentrated in one neighborhood"
        ]
    },
    "spot-024": {
        "name_en": "Inunaki Mountain Tunnel",
        "prefecture_en": "Ōsaka Prefecture",
        "city_en": "Izumisano City",
        "summary_en": "The Inunaki (\"Howling Dog Mountain\") complex in southern Ōsaka Prefecture is unusual in that its supernatural reputation derives directly from its historical identity as a sacred site of Shugendo mountain asceticism — a training ground for yamabushi (mountain monks) opened more than 1,300 years ago by the monk En no Gyōja, Japan's patron of mountain religion. The tunnel that carries the old road through the mountain has accumulated the specific reputation of a portal where the rules of ordinary reality become negotiable: mirrors are said to show things they shouldn't; engines die without explanation; passengers feel the presence of riders who were not there at the beginning of the journey. The tunnel sits within a still-functioning sacred complex whose temple (Shippōryūji) continues to be used for ritual training, creating an unusual overlap between active religious practice and ghost tourism. The sincerity of one does nothing to diminish the atmosphere of the other.",
        "highlights_en": [
            "\"Do not look in the rearview mirror\" — this specific, actionable piece of haunted-tunnel advice implies a confidence in the story that demands attention",
            "The tunnel sits inside a 1,300-year-old Shugendo sacred mountain: the spiritual density is not manufactured for tourism but accumulated over millennia",
            "The most credibly \"real\" haunted site in Ōsaka Prefecture, by consensus of those who track such things"
        ]
    },
    "spot-025": {
        "name_en": "Nuezuka (The Nue's Burial Mound)",
        "prefecture_en": "Ōsaka Prefecture",
        "city_en": "Ōsaka City, Kita Ward",
        "summary_en": "The nue — a chimeric creature with the head of a monkey, the body of a tanuki, the tail of a snake, and the legs of a tiger — is Japan's most conceptually interesting monster. Its name has entered modern Japanese as a metaphor for anything that resists categorization: political positions, unnameable anxieties, identities that refuse easy description. According to the Heike Monogatari, the warrior Minamoto no Yorimitsu shot this creature from the night sky over the Imperial Palace in the 12th century, and its body, loaded onto a boat, drifted down what is now the Dōjima River until it grounded somewhere in present-day Ōsaka. Multiple mounds across the city claim to be the burial site of the creature's remains. The exact locations are now uncertain — urban development has moved, paved over, or simply lost most of them — but the tradition of marking the nue's presence persists in neighborhood customs and street-name etymologies. What this means in practice is that the monster's bones are somewhere beneath Ōsaka's neon-lit entertainment district, in a subterranean presence that the city has chosen, characteristically, to remember by continuing to argue about where exactly they ended up.",
        "highlights_en": [
            "Multiple mounds across central Ōsaka claim to contain the remains of Japan's most conceptually significant monster",
            "The word \"nue\" has entered modern Japanese as a metaphor for anything unclassifiable — visiting the burial site feels like touching the origin of a metaphor",
            "The contrast between the monster's burial in the depths of Japan's most energetically commercial city is an image worth sitting with"
        ]
    },
    "spot-026": {
        "name_en": "Shirataka Ōkami Abandoned Shrine",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Nara City",
        "summary_en": "In a residential neighborhood of Nara City, down a narrow lane that gives no indication of what lies ahead, a small pond complex opens into what was once the head shrine of a new religious movement founded in the Meiji period by a spirit medium named Nakai Shigeno. Her \"Tamahime Kyōkai\" (Princess Soul Church) was an independent Shinto movement that drew followers for decades before declining, leaving behind a complex of concrete-reinforced sacred pools, a small waterfall, and a collection of unusual deities — White Dragon, Old Woman, and others of uncertain canonical status — whose stone markers still stand among the vegetation. The atmosphere of a once-visited and now-forgotten sacred place is exceptionally strong here, amplified by the site's position inside an otherwise normal neighborhood: the transition from suburban street to overgrown shrine precinct takes about twelve steps and crosses a temporal distance of roughly a century. This is Nara Prefecture's most widely cited haunted site, though its appeal to those without supernatural interests is considerable.",
        "highlights_en": [
            "A Meiji-era spirit medium's personal shrine complex, abandoned and slowly returning to nature inside an otherwise ordinary neighborhood",
            "The deities honored here — White Dragon, Ancient Woman, others — exist outside mainstream Shinto taxonomy, creating a genuinely heterodox spiritual atmosphere",
            "The transition from normal suburban street to this place happens in a few steps; the psychological transition takes rather longer"
        ]
    },
    "spot-027": {
        "name_en": "Former Maya Kanko Hotel (\"Mayakan\")",
        "prefecture_en": "Hyōgo Prefecture",
        "city_en": "Kōbe City, Nada Ward",
        "summary_en": "Built in 1929 at the midpoint of Mount Maya above Kōbe, the Maya Kanko Hotel was an Art Deco vision of mountain luxury — a destination resort accessible only by cable car, its terraces commanding views of the bay and the Ōsaka plain. It operated until 1993. Since then, the forest has been steadily reclaiming it in what can only be described as a collaboration between architectural history and botanical patience, and the result is what urban explorers and cultural commentators have called, without any apparent irony, the most beautiful ruin in Japan. In 2021, the abandoned hotel was designated a Registered Tangible Cultural Property by the Japanese government — a recognition that a ruin, as a ruin, can have cultural value sufficient to merit official protection. This is, to put it mildly, an unusual administrative position, and it reflects the degree to which Mayakan has become a genuinely beloved object in Japanese cultural life. Access is normally restricted, but guided tours are occasionally organized through heritage groups.",
        "highlights_en": [
            "Registered as a Tangible Cultural Property while remaining an active ruin — a contradiction that the Japanese government resolved in favor of the building",
            "The Art Deco architecture and the forest's reclamation have achieved a visual harmony described by virtually every visitor as \"like a Ghibli film\"",
            "The title \"Queen of Ruins\" is not hyperbole: the combination of architectural quality, setting, and abandonment history is unmatched in Japan"
        ]
    },
    "spot-028": {
        "name_en": "Tomogashima Island Fortifications (Old Imperial Army Ruins)",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Wakayama City, Kada",
        "summary_en": "Twenty minutes by ferry from the fishing town of Kada, the uninhabited island of Tomogashima holds the ruins of a coastal defense fortress built by the Imperial Army beginning in 1884, intended to guard the Kii Channel against naval invasion and never tested in actual combat. The ruins — brick powder magazines, artillery emplacements, concrete command posts — have been consumed over decades by the island's subtropical forest, creating a landscape where military infrastructure and nature have merged into something that several million people recognize from Hayao Miyazaki's Laputa: Castle in the Sky. Whether or not Miyazaki specifically had Tomogashima in mind, the visual correspondence is striking enough that the island serves as an unofficial pilgrimage site for fans of the film. It is also the setting of the anime Summer Time Rendering, and its selection as one of the \"88 Anime Sacred Sites\" in 2022 has brought new categories of visitor to a site that already had ample reason to attract them.",
        "highlights_en": [
            "Brick vaulted powder magazines and gun emplacements consumed by tropical vegetation — the image that appears in every description of what Laputa's ruins actually look like",
            "A fortress that was built for a war that never came, and survived instead to become a forest: the melancholy of unused military infrastructure at its most photogenic",
            "Pilgrimage site for fans of Castle in the Sky AND Summer Time Rendering — rare multi-franchise sacred ground"
        ]
    },
    "spot-029": {
        "name_en": "Kifune Shrine (Birthplace of Ushi no Koku Mairi Curse Ritual)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Sakyō Ward",
        "summary_en": "Kifune Shrine is nationally famous as a place of water deity veneration and romantic matchmaking — its menu of dedicated love-fortune fortunes includes a type printed in ink visible only when the paper is floated in water, which is charming and photogenic and heavily marketed. It is also the canonical birthplace of ushi no koku mairi, the curse ritual in which a white-robed figure drives iron nails through a straw effigy at the witching hour, and is widely understood to be the site where this practice continues to be enacted in secret. The relationship between these two functions — love shrine and curse site — is not, in the Japanese religious imagination, as contradictory as it might seem: Kifune is a shrine of deep emotional power, and deep emotional power cuts in multiple directions. The river valley location becomes entirely different at night. The darkness that closes over the path from the main road to the inner shrine in the small hours is the kind of darkness that reminds you of exactly how much light you normally depend on.",
        "highlights_en": [
            "The same shrine venerates love and love's destruction: the coexistence of romantic matchmaking and active curse practice is not ironic in the Japanese religious framework but simply honest",
            "Reports of ushi no koku mairi being practiced at night are not historical anecdotes but current news — the tradition is ongoing",
            "The valley at night offers one of Kyōto's most genuinely atmospheric experiences: the light is gone, the traffic is gone, and the shrine's character is entirely different"
        ]
    },
    "spot-030": {
        "name_en": "Fushimi Inari Taisha — Inner Sanctuary Beyond the Crowds",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Fushimi Ward",
        "summary_en": "The thousand torii gates of Fushimi Inari have become one of the most-photographed images in Japan, which means that approximately ninety percent of visitors photograph the lower gates and leave without discovering what the shrine actually is. The fox deity Inari's mountain is a two-hour vertical ascent, and as altitude increases, crowds diminish and the religious density increases. Past the inner sanctuary the torii thin and the path enters zones where weathered wooden votive tablets and stone fox messengers accumulate in arrangements that were not designed for Instagram, and carry a quality of genuine sacred ecology that no amount of orange lacquered lumber at the base can communicate. At the summit, 233 meters up through the forest, the mountain's character is fully legible: this is a living site of active popular religious practice, visited by thousands of supplicants daily, whose requests for business success, health, and harvest fill the votive boards on every post. The tension between the world-famous tourist attraction at the bottom and the working sacred mountain at the top is one of Japan's most instructive contrasts.",
        "highlights_en": [
            "The two-hour ascent to the summit sheds nearly all tourist infrastructure and deposits you in a functioning sacred mountain that looks nothing like the postcard",
            "Beyond the inner sanctuary, the accumulation of weathered stone foxes and wind-damaged votive tablets creates an atmosphere of genuine spiritual intensity",
            "The most-visited shrine in Japan has a second, almost entirely unvisited face — and it is the more interesting one"
        ]
    },
    "spot-031": {
        "name_en": "Zutō (Nara's Pyramid)",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Nara City",
        "summary_en": "In a residential neighborhood of Nara City, between ordinary houses and municipal roads, a stepped seven-layer earthen pyramid rises 10 meters from the ground, its sides measuring 32 meters, its construction dating to the Nara Period (roughly 1,300 years ago). The Zutō — \"Head Mound\" — takes its name from a story that has haunted the site ever since its telling: the monk Genbō, a politically controversial figure of the 8th century, was said to have had his severed head fall from the sky after his death. The head was buried here. Each layer of the pyramid holds stone Buddha images, and the overall structure defies clean categorization in any school of Nara Buddhist architecture. Why it was built in this specific form — a stepped pyramid surrounded by ordinary houses, visible from the road and apparently hiding in plain sight — is a question that continues to agitate historians and attracts a reliable stream of visitors from the Ancient-Mystery end of the tourism spectrum.",
        "highlights_en": [
            "A monk's decapitated head fell from the sky and was buried here — the founding legend sets the tone for an experience that does not disappoint",
            "A 1,300-year-old stepped pyramid in a Nara residential neighborhood: the visual impact of this juxtaposition is immediate and permanent",
            "300-yen admission to one of the stranger things you can stand next to in Japan"
        ]
    },
    "spot-032": {
        "name_en": "Sakafune-ishi and Kamekata Stone Artifacts",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Asuka Village, Takaichi District",
        "summary_en": "The Asuka Period (roughly 538–710 CE) was one of the most consequential eras in Japanese history — a time of Buddhist introduction, administrative reform, and the construction of the first permanent capitals. It was also, apparently, a time of extensive stone carving whose purpose has not been explained in 1,400 years. The Sakafune-ishi (\"Sake-Boat Rock\") is a granite slab 5.5 meters long and 2.3 meters wide, carved with channels, grooves, and depressions that suggest — depending on the theorist — sake production, pharmaceutical processing, astronomical instrumentation, or garden hydraulics. Adjacent, the Kamekata Stone Artifacts (\"Turtle-shaped\" ritual pools) are elaborate water-circulation devices whose ceremonial function is better understood but whose specific ritual context remains debated. Together they anchor an entire tradition of ancient-mystery tourism that unfolds across the Asuka Valley, where the density of unexplained carved rocks per square kilometer reaches a level genuinely without parallel in the ancient world.",
        "highlights_en": [
            "Nobody knows what Sakafune-ishi was for — and this is not a failure of research but a genuine, 1,400-year-old mystery with multiple active scholarly camps",
            "The turtle-shaped stone basin with functional water channels represents a level of ritual hydraulic engineering whose elegance is apparent even without knowing its purpose",
            "Asuka Valley is effectively a \"mystery rock district\" — Sakafune-ishi is the anchor of a circuit that fills a full day"
        ]
    },
    "spot-033": {
        "name_en": "Masuda no Iwafune (Masuda's Rock Boat)",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Kashihara City",
        "summary_en": "On a hilltop in Kashihara City, on the southern edge of the Asuka Valley, sits an 800-ton granite boulder so large that its own geology seems insufficient explanation for its presence. It measures 11 meters by 8 meters at the base and stands approximately 4.7 meters tall; its upper surface has been carved with two circular pits each about 1 meter in diameter and 1 meter deep, connected by a channel, alongside a network of surface grooves whose function no scholar has satisfactorily explained. The boulder's name — \"Masuda's Rock Boat\" — derives from a tradition that enormous stones arrived in Asuka from the sky, delivered by forces that ordinary earthbound labor could not account for. The carving is clearly the work of human hands, probably Imperial-era, but the original purpose of the two deep pits remains entirely open: tomb preparation, astronomical alignment device, water ritual basin, and ritual mirror stand have all been proposed, and none has prevailed. Active archaeological research continues.",
        "highlights_en": [
            "Two meter-deep pits carved into the top of an 800-ton boulder — and no one, after more than a millennium of looking, knows why",
            "\"Rock Boat\" implies descent from the sky: the name carries the conceptual DNA of an ancient worldview in which stones arrived from elsewhere",
            "The most unresolved of all Asuka's many mystery rocks, and the one that most reliably inspires the sense that something significant has been forgotten"
        ]
    },
    "spot-034": {
        "name_en": "Takeda Castle Ruins (Castle in the Sky)",
        "prefecture_en": "Hyōgo Prefecture",
        "city_en": "Asago City",
        "summary_en": "The ruins of Takeda Castle are frequently described as \"Japan's Machu Picchu,\" which is accurate in form but omits what makes the site genuinely strange: the thing being photographed is a 15th-century abandoned castle, reduced to its stone foundations, that happens to be enveloped in sea-cloud formations on autumn and winter mornings in a way that makes the ruins appear to float. There is no reconstruction. No historically dressed guides. No gift shop at the summit. There is a steep mountain trail, a pre-dawn departure time, and the absolute requirement of luck with the weather — all of which means that the experience of actually seeing Takeda Castle in its cloud-surrounded state requires commitment. This commitment is, in some respects, the experience: the cold, the dark, the possibility that the clouds won't form or will burn off before you arrive, all conspire to make successful viewing feel less like tourism and more like an event that the mountain chose to allow.",
        "highlights_en": [
            "Pre-dawn hiking to wait for a cloud inversion that may or may not materialize: a form of pilgrimage patience with no guaranteed payoff",
            "Stone foundations of a 600-year-old abandoned castle floating above the clouds — the gap between the site's modest material reality and its visual impact is one of Japan's great optical phenomena",
            "A famous tourist destination that has successfully resisted the temptation to become comfortable: the mountain still demands its toll"
        ]
    },
    "spot-035": {
        "name_en": "Kōyasan Okunoin (Mount Kōya Inner Sanctuary)",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Kōya Town, Ito District",
        "summary_en": "Kōbō Daishi — the monk Kūkai — founded Mount Kōya's Buddhist complex in 819 CE, entered a state of eternal meditative samādhi in 835 CE, and by the faith of the Shingon school, has not died since. He waits in his mausoleum at Okunoin, the innermost sanctuary of the mountain, sustained by monks who deliver food and change his robes twice daily. The two-kilometer path leading to the mausoleum passes through the largest cemetery in Japan, containing more than 200,000 grave markers, memorial stones, and cenotaphs donated by feudal lords, Edo-period merchants, modern corporations, and ordinary families across twelve centuries of devotion. Walking this path at night — which is entirely permitted and regularly done — delivers one of the most genuinely affecting experiences available on the Japanese archipelago: the path is lit by stone lanterns, the cedars are enormous, and the sense of being in the presence of something accumulative and vast and still operating is difficult to dismiss regardless of one's religious convictions. It was designated a UNESCO World Heritage Site in 2004.",
        "highlights_en": [
            "Kūkai has been in continuous meditative sleep since 835 CE, tended by monks daily — the concept of a living saint generating 1,200 years of active pilgrimage is one of Japan's most extraordinary religious facts",
            "200,000 grave markers along a two-kilometer forest path, including the cenotaphs of warlords, saints, and corporate entities — a cross-section of Japanese civilization's entire duration",
            "Night walking between stone lanterns in Japan's greatest cedar-forest cemetery: an experience that operates at a register most travel does not reach"
        ]
    },
    "spot-036": {
        "name_en": "Tamaki Shrine",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Totsukawa Village, Yoshino District",
        "summary_en": "Tamaki Shrine sits at 1,076 meters in the Ōmine mountain range — Japan's sacred mountain spine — in one of the most remote and logistically demanding corners of Honshu. The standard approach by road involves approximately 90 minutes of mountain driving after the nearest expressway exit, through terrain that progressively surrenders human-scale infrastructure. Drivers report GPS devices losing signal. Sudden fog. An incline of expectation that builds in proportion to the difficulty of the journey. The shrine complex, when reached, has the quality of a place that does not need to impress you: enormous ancient cedars flank a simple hall, the air is different, the silence is specific. Tamaki is widely described in Japanese spiritual discourse as a shrine that operates by selection — people who try to visit frequently find the road blocked, the weather uncooperative, the journey frustrated by circumstances that feel somehow non-random. Whether or not this is true in any verifiable sense, the shrine's inaccessibility performs a reliable filtering function that ensures its atmosphere is never diluted by casual drop-in tourism.",
        "highlights_en": [
            "\"You cannot go unless you are called\" — a concept that functions as both a spiritual claim and a logistical reality in one of Japan's most remote shrine locations",
            "The Ōmine mountain range's deepest recesses: a genuine sacred wilderness rather than a packaged pilgrimage",
            "Ancient cedars, specific silence, altered air — reported by visitors across centuries and across cultural backgrounds with striking consistency"
        ]
    },
    "spot-037": {
        "name_en": "Tenkawa Benzaiten Shrine",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Tenkawa Village, Yoshino District",
        "summary_en": "The goddess Benzaiten — deity of music, eloquence, art, and water — is enshrined in three locations celebrated as Japan's greatest Benzaiten sites, and the Tenkawa version is arguably the strangest of them. Accessible only by mountain road through the village of Tenkawa, which sits in a river valley surrounded by the Ōmine range with no practical public transport connection, the shrine has accumulated a reputation among musicians, writers, and artists as a place whose gravitational pull operates outside normal explanatory frameworks. People describe deciding on impulse to go; finding themselves there without entirely intending to arrive; returning repeatedly without being able to articulate the reason. The shrine's main treasure is the Go-ju-suzu, a set of sacred bells designated as a National Treasure, whose sound is said to affect the space it inhabits in ways that go beyond acoustics. Whether or not this is experience or suggestion is, at Tenkawa, beside the point: the valley itself, the shrine's placement within it, and the quality of the journey required to get there create conditions under which the ordinary categories of tourist experience cease to apply.",
        "highlights_en": [
            "Musicians and artists report being drawn here by forces they cannot name — a consistency of testimony that deserves more attention than rational skepticism can comfortably dispense",
            "The National Treasure Go-ju-suzu bells: sacred sound as material cultural heritage, experienced in the mountain valley that amplifies everything",
            "One of Japan's true hidden sacred sites — genuinely difficult to reach, genuinely worth the effort"
        ]
    },
    "spot-038": {
        "name_en": "Hashigui-iwa (Bridge Pillar Rocks)",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Kushimoto Town, Higashimuro District",
        "summary_en": "For 850 meters offshore from the tip of the Kii Peninsula, more than forty rock columns rise from the sea in a formation so regular that it reads as the remnant of a deliberate construction project rather than a geological accident. The legend explains it accordingly: the monk Kūkai (Kōbō Daishi) wagered with an evil deity (an amanojaku) that neither could build a bridge to the island of Ōshima in a single night — the deity to construct the pilings, Kūkai to string the span. The deity completed its work; Kūkai, seeing what had been accomplished, employed a theological maneuver to void the bet; the unspanned pillars remain as evidence. The rocks are a Natural Monument and a National Site of Scenic Beauty, formally recognized for their geological interest, but the legend does more explanatory work than the volcanology. At low tide, you can walk among the base of the columns. At dawn, with the sun rising from behind the island of Ōshima and silhouetting the rock row against orange water, the bridge-that-never-was achieves a visual completeness that the completed bridge would probably have lacked.",
        "highlights_en": [
            "Forty-plus rock columns marching into the sea in formation — a geological accident that has the visual grammar of a deliberate monument",
            "Kūkai versus the evil deity: a legend that explains the landscape better than the geology does, and feels more true in the presence of the rocks",
            "Dawn at Hashigui-iwa is an experience in the highest tier of natural photography in Japan — and remains less crowded than its quality deserves"
        ]
    },
    "spot-039": {
        "name_en": "Nachi-no-Taki (Nachi Falls — The God That Falls)",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Nachikatsuura Town, Higashimuro District",
        "summary_en": "The Nachi Falls are Japan's tallest single-drop waterfall at 133 meters, and they are also a god. This is not metaphor. The falls constitute the principal object of veneration for the subordinate shrine of Kumano Nachi Taisha, designated a National Treasure — one of the only waterfalls in the world recognized as both a natural and cultural UNESCO World Heritage site specifically because of its identity as an active deity rather than just a scenic feature. The distinction between looking at a waterfall and standing in the presence of a god is, at Nachi, a distinction that the site's entire architectural and ritual organization refuses to let you treat as merely semantic. The Hirokū Shrine (Hiro Shrine) sits at the base of the falls, its torii standing directly in the cascade's mist, its offerings left for a deity whose voice is the continuous sound of water on rock. The scale of the falls — visible from the sea, audible from a kilometer away — created the conditions for worship long before anyone articulated a theology around them, and those conditions are entirely intact.",
        "highlights_en": [
            "The fall is not beside a shrine — the fall IS the shrine: a primary deity in active service as a 133-meter column of falling water",
            "The Hiro Shrine torii stands in the waterfall's mist; the \"water of eternal life\" drawn from the falls has been offered to pilgrims for over a thousand years",
            "A sacred site whose power operates regardless of one's religious convictions — the scale and sound of the falls make their own argument"
        ]
    },
    "spot-040": {
        "name_en": "Tsubaki Grand Shrine (Inner Sanctuary and Kanae Waterfall)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Suzuka City",
        "summary_en": "The Tsubaki Grand Shrine (Tsubaki Ōkami Yashiro) is the national head shrine of Sarutahiko-no-Ōkami — the colossal, long-nosed deity who guided the gods' descent to earth and serves in Japanese mythology as the patron of crossroads, journeys, and destiny's opening. The main shrine complex is impressive in the way that large, well-maintained ancient shrines are impressive, but the real draw for those willing to walk the additional twenty minutes into the mountain is the Oku-no-Miya (inner sanctuary) and the small Kanae Falls beyond it. At the inner sanctuary, the forest changes character in the way that forests around genuinely old sacred sites sometimes do: the cedars become larger, the light becomes different, the quality of quiet becomes active rather than passive. The falls themselves are modest in scale but situated at a point where the path's increasing steepness, the narrowing of the cedar canopy, and the sound of water converging all conspire to produce the specific sensation associated with genuine mountain pilgrimage. As the most accessible major power spot from Kameyama, Tsubaki offers full sacred-mountain experience within a thirty-minute drive.",
        "highlights_en": [
            "The most accessible serious power spot from Kameyama — everything that takes hours elsewhere is here in 30 minutes",
            "The inner sanctuary and Kanae Falls add a genuine mountain-pilgrimage register to what begins as an ordinary shrine visit",
            "Free entry to a complex large enough to occupy two to three hours: one of the best value-to-experience ratios in Mie Prefecture"
        ]
    },
    "spot-041": {
        "name_en": "Maruyama Senmaida (Thousand-Layered Rice Terraces)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Kumano City",
        "summary_en": "The Maruyama Senmaida is not the largest rice terrace system in Japan, but its configuration — 1,340 individual paddy fields stacked on a steep slope in the mountain interior above Kumano, each field roughly the size of a large room — produces a visual effect of accumulated human obsession that is difficult to process in rational terms. Someone decided to farm this slope. Then someone else did. The decision was repeated 1,340 times, over roughly a thousand years, by people who could reasonably have found flatter ground somewhere more accessible. What exists now is both a landscape and an argument: evidence that human agricultural willpower, applied with sufficient concentration over sufficient time, can reconfigure the surface of a mountain. In May, the paddies fill with water and reflect the sky in a thousand separate mirrors. In October, after harvest, the terraces are illuminated after dark with candles — an event that turns the hillside into something the word \"scenic\" inadequately describes.",
        "highlights_en": [
            "1,340 rice paddies on a single mountain slope — a millennium of agricultural accumulation that reads as a feat of collective obsession",
            "The October candlelit illumination of the harvest terraces is one of the most visually transcendent nighttime experiences in rural Japan",
            "The terrace ownership program allows visitors to tend their own paddy: agricultural participation that connects you to the landscape's thousand-year logic"
        ]
    },
    "spot-042": {
        "name_en": "Onigajō (Demon's Castle Sea Caves)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Kumano City",
        "summary_en": "For one kilometer along the Pacific coast south of Kumano City, the sea has spent several million years carving the sedimentary cliffs into a succession of caves, arches, overhangs, and sea stacks whose vertical walls are striated in horizontal bands like a geological textbook illustration. The Onigajō (\"Demon's Castle\") is the name given to the entire formation, based on the tradition that this coast was the stronghold of the pirate-warlord Tagazaru, whose subjugation by the general Sakanoue no Tamuramaro was reframed in legend as a battle against demons. A coastal walkway threads through the cave system, passing under arches where the ceiling is perforated by sea-carved holes that frame oval windows of sky. The effect — of walking through the interior of a geological process that is still, technically, ongoing — is of the specific kind of awe that has nothing to do with human achievement. The site is part of the Kumano Kodō UNESCO World Heritage zone, and remains significantly less crowded than its quality warrants.",
        "highlights_en": [
            "Walking for a kilometer through sea caves with sky visible through eroded ceiling holes — the sensation of being inside an ongoing geological event",
            "The roof collapses that created the cave windows are simultaneously the evidence of erosion and the source of the site's most extraordinary views",
            "UNESCO World Heritage site with the paradoxical advantage of low visitor numbers — a genuinely uncrowded encounter with a remarkable landscape"
        ]
    },
    "spot-043": {
        "name_en": "Shishi-iwa (Lion Rock)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Mihama Town, Minamimuro District",
        "summary_en": "Twenty-five meters of granite emerge from the water at the edge of the Kumano coastal road with a profile that, from the designated viewing angle, reproduces the face of a lion — or more specifically, an open-mouthed lion at the exact moment of an aggressive roar — with a completeness of resemblance that makes the naturalistic explanation feel insufficient. The rock is a National Monument and sits along the Kumano Kodō pilgrimage route, meaning that travelers en route to Kumano's sacred sites have been pausing here for well over a thousand years, and have had a thousand years to consider what it means that a sea-carved rock happens to wear the face of a divine predator. The practical answer to why rocks that look like things become sacred is embedded in a rock that looks, very specifically, like this.",
        "highlights_en": [
            "The resemblance to a roaring lion is not approximate but exact — the kind of natural face that converts skeptics",
            "Situated on the Kumano Kodō pilgrimage road, pilgrims have been pausing at this rock for over a thousand years",
            "The rock concisely demonstrates why natural landscape features become sacred objects: if you stood before it and it looked like nothing, it would still be worth looking at"
        ]
    },
    "spot-044": {
        "name_en": "Taga Taisha Shrine",
        "prefecture_en": "Shiga Prefecture",
        "city_en": "Taga Town, Inugami District",
        "summary_en": "The deities of Taga Taisha are Izanagi and Izanami — the primordial couple who created the Japanese archipelago, who gave birth to the sun goddess and the moon deity and the sea deity and the storm deity and, accidentally, the fire deity whose birth killed Izanami. They are, in other words, the ultimate ancestors of everything that matters in the Japanese cosmological imagination. The Grand Shrine of Ise, to which every Japanese person has a nominal familial relationship, houses Izanagi's daughter. Taga Taisha houses the parents. Historically, this was understood to carry corresponding weight: a Edo-period folk song enumerated \"Seven visits to Ise, three visits to Kumano, monthly visits to Taga\" in that order, suggesting that Taga was a destination visited more frequently than either of Japan's most famous sacred sites. The shrine's contemporary relative obscurity — leafy and peaceful, with far fewer visitors than its mythological pedigree should attract — makes it simultaneously a genuine off-the-beaten-path discovery and a mild puzzle about the relationship between a site's intrinsic significance and its popular recognition.",
        "highlights_en": [
            "The parents of Amaterasu and creators of Japan are enshrined here — a mythological pedigree that places Taga at the origin of everything in the Japanese pantheon",
            "Historical folk tradition ranked Taga as a more frequent pilgrimage destination than Ise itself — the gap between that status and its current quietude is the shrine's most interesting quality",
            "A peaceful, unhurried sacred space whose tranquility is all the more striking given what it contains"
        ]
    },
    "spot-045": {
        "name_en": "Yōrō Falls and the Legend of the Drunkard's Discovery",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Yōrō Town, Yōrō District",
        "summary_en": "In the early 8th century, according to a tale recorded in historical chronicles, a poor woodcutter discovered a waterfall in the mountains above what is now Yōrō whose water tasted of sake. He brought some home to his elderly father, who drank it and experienced remarkable rejuvenation. The Emperor Genshō, learning of this miraculous waterfall, changed the era name to \"Yōrō\" (\"Aged Care\") in 717 CE — an era name still attached to this town, this mountain, and this waterfall. The waterfall itself is genuine, attractive, and part of a well-developed nature park. The legend is magnificent. The proximity of the Yōrō Tenmei Aichi (Reversible Destiny Lofts), the Chinpin Castle, and this waterfall — all within a few kilometers of each other — creates a zone of concentrated absurdist logic unique in the Tōkai region, making Yōrō Town the single highest-density odd attraction per square kilometer in the region.",
        "highlights_en": [
            "The origin legend of an era name: water that turned to sake, a father restored to health, and a grateful Emperor who changed the calendar in response",
            "Combine with the Reversible Destiny Lofts and Chinpin Castle for the complete Yōrō Oddity Circuit — three genuinely strange things within a few kilometers",
            "The falls themselves are legitimately beautiful: a rare case where the legend and the landscape both fully deliver"
        ]
    },
    "spot-046": {
        "name_en": "Shirakawa-gō (Hinamizawa Village — The Higurashi Model)",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Shirakawa Village, Ōno District",
        "summary_en": "Shirakawa-gō's UNESCO-listed gassho-zukuri farmhouses — their dramatically steep thatched roofs designed to shed the region's famous deep snowfall — have been a World Heritage site since 1995 and among the most photographed traditional settlements in Japan. Less frequently noted is that the village's combination of physical isolation (mountains on all sides, a single road in), collective social organization (the traditional yui system in which neighbors cooperate on roof maintenance), and a quality of visual perfection that feels slightly too composed has made it the recognized model for Hinamizawa, the fictional village in the horror-mystery visual novel and anime series Higurashi no Naku Koro ni. The franchise explicitly acknowledges the connection and has generated a substantial pilgrimage tourism to the site. In winter, when Shirakawa-gō receives snowfall that genuinely cuts it off from the outside world, and after the last tourist buses have departed, the village's other face — the one that is less a heritage site than an actual closed community with its own social codes and generational memory — becomes briefly visible.",
        "highlights_en": [
            "The confirmed setting for the village of Hinamizawa in Higurashi no Naku Koro ni — a pilgrimage for fans of one of Japan's most influential horror franchises",
            "Under winter snowfall and after tourist hours, the village's World Heritage presentation dissolves and something older and more opaque takes its place",
            "The aerial view from the designated observation point produces an involuntary sensation of unreality — a settlement too geometrically perfect to be entirely real"
        ]
    },
    "spot-047": {
        "name_en": "Izu Gokurakuen (Izu Paradise Garden — Hell and Heaven Dioramas)",
        "prefecture_en": "Shizuoka Prefecture",
        "city_en": "Izu City",
        "summary_en": "Since 1986, the family-run Izu Gokurakuen has been offering visitors a guided tour through Buddhist hell and heaven rendered in roughly 300 life-sized dioramas. The eight great hells of Buddhist cosmology — with their specific torments for specific sins — are reproduced with a specificity and conviction that suggests the creators took their theological brief seriously, even as the homemade quality of the execution gives the whole enterprise a warmth that professional production would have destroyed. Enma Daiō (the Great Judge of the Dead) sits in his courtroom; the River Sanzu divides this world from the next; sinners undergo their appointed punishments with a range of expressions from anguished to resigned. A secondary exhibit, restricted to visitors over 18, covers erotic Buddhist cosmology in a register that connects the facility to the hihoukan tradition of Shōwa-era resort entertainment. The combination — hell, heaven, and the taxonomy of human desire, all in a single family-run facility fifteen minutes from Shuzenji hot spring — is a capsule statement about the range of things Japanese folk religion has always been able to hold simultaneously.",
        "highlights_en": [
            "The Eight Great Hells of Buddhist cosmology reproduced at life scale in a family-run facility — theological ambition delivered with handmade sincerity",
            "Enma Daiō, the great judge of the dead, rendered in a format that is both spiritually serious and entirely approachable",
            "A hell-and-heaven tour followed by an adults-only erotic cosmology exhibit: the full range of Japanese folk Buddhism in one building"
        ]
    },
    "spot-048": {
        "name_en": "Ryūgū Cave (Dragon Palace Cave — Heart-Shaped Skylight)",
        "prefecture_en": "Shizuoka Prefecture",
        "city_en": "Minami-Izu Town, Kamo District",
        "summary_en": "The Ryūgū Cave at Irōzaki on the Izu Peninsula is a sea cave whose ceiling collapsed at some point in the geological past, creating an opening that — viewed from inside the cave, looking up at the sky — forms a near-perfect heart shape. This is entirely unplanned. The heart is the product of coastal erosion removing rock in a configuration that no designer could have contrived, which is part of why it became an Instagram phenomenon before Instagram was a word: the image of a heart-shaped window to blue sky, framed by dark volcanic cave walls, with the sound of the Pacific moving through the cave's acoustic space, has an involuntary emotional impact regardless of one's cynicism about heart-shaped tourist traps. At low tide, a sand beach is accessible at the cave's base. The cave's name — Dragon Palace — comes from the Urashima Tarō folk legend, Japan's version of the time-dilating underwater paradise story, which is an appropriately surreal mythological frame for a geological accident this pretty.",
        "highlights_en": [
            "A collapsed sea-cave ceiling producing a heart-shaped sky window — not designed, not manufactured, not imagined by anyone: purely accidental and genuinely striking",
            "The acoustic space of the cave with Pacific Ocean waves resonating through it creates a sensory experience that photographs cannot reproduce",
            "At low tide, the sand at the cave's base is accessible — close-up contact with an otherwise aerial phenomenon"
        ]
    },
    "spot-049": {
        "name_en": "Birthplace of the Tobidashi Bōya (Pop-Out Boy Traffic Signs)",
        "prefecture_en": "Shiga Prefecture",
        "city_en": "Higashiōmi City",
        "summary_en": "The flat, brightly colored silhouette of a child running into the road — the tobidashi bōya (\"pop-out boy\") traffic warning sign — is so ubiquitous in Japan that it has achieved the paradoxical invisibility of the truly familiar. What very few people know is that every one of these signs traces back to a single source: Shiga Prefecture's Higashiōmi City, where a sign painter named Kudoku began making them in 1973 as a personal contribution to road safety, distributing them at his own expense to intersections near schools. Shiga Prefecture now hosts more than 1,000 of them per square kilometer — more, per capita, than any prefecture in Japan — and has spawned an entire regional cottage industry of variants: local mascot versions, historical character versions, festival-character versions. The origin site in Higashiōmi preserves the original designs alongside the evolutionary tree of 50-plus years of local iteration. This is the origin story of something so omnipresent it stopped being noticed.",
        "highlights_en": [
            "A sign painter's personal 1973 campaign to prevent traffic deaths created an icon so successful it colonized the entire country — and almost no one knows it came from here",
            "Shiga Prefecture's tobidashi bōya density is the highest in Japan; walking through certain neighborhoods is like walking through a convention",
            "The local variant ecosystem — Hikone Castle mascot bōya, ancient messenger bōya, festival character bōya — represents 50 years of folk art iteration on a single graphic"
        ]
    },
    "spot-050": {
        "name_en": "Gifu Retro Museum",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Yamagata City, Gifu",
        "summary_en": "A converted school building in the hills of Yamagata City, Gifu Prefecture contains 200-plus pieces of Shōwa-era game and vending machine history, most of them operational, all of them representing the specific flavors of entertainment technology that Japan produced and largely abandoned between the 1960s and 1990s. The operative word is \"operational\": this is not a collection of objects behind glass but a functioning arcade of antique machines in which a 1970s pinball game, a 1980s medal shooter, and — most improbably — a hot-food vending machine dispensing ramen and toast in their original Shōwa configurations can all be played, operated, and consumed during a single visit. The time-based admission system (1,000 yen per hour) creates a specific relationship with the material that conventional admission models do not: you are buying time inside an era rather than access to a collection. For those to whom the retro-Japan aesthetic is not nostalgia but archaeology, the Gifu Retro Museum offers a density of first-hand material that no amount of reading about the period replicates.",
        "highlights_en": [
            "Shōwa-era hot-food vending machines — ramen, toast, canned goods — still operational and still selling: the most edible form of time travel available",
            "200-plus vintage arcade and game machines in active operation: a working museum of an entertainment technology that no longer exists outside places like this",
            "The converted school building amplifies the temporal dislocation — the architecture of childhood combined with the entertainment technology of a specific childhood era"
        ]
    }
}

# ─────────────────────────────────────────────
# FESTIVALS TRANSLATIONS
# ─────────────────────────────────────────────

FESTIVALS_EN = {
    "fest-001": {
        "name_en": "Hōkaiji Naked Dance (Shushōe Ceremony)",
        "shrine_en": "Hōkaiji Temple (Hino Yakushi)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Fushimi Ward",
        "date_pattern_en": "Annual, January 14th",
        "summary_en": "At a small Buddhist temple in the southern hills of Kyōto, a ceremony has been conducted on the night of January 14th since the late Heian Period — a night-ritual of such intimacy and physical immediacy that it operates at a completely different register from the large-scale bizarre festivals that dominate Japan's international coverage. Hōkaiji (known locally as Hino Yakushi, the Yakushi Buddha of Hino) conducts the final night of the Shushōe, a January Buddhist purification rite, with a ceremony in which men clad only in fundoshi (loin cloths) link arms inside the main hall and circle the Yakushi Buddha, chanting \"chōraku, chōraku\" — \"eternal joy, eternal joy\" — while the crowd presses in close enough to feel the heat of their bodies. The scale is small, the crowd is dense, and the boundary between observer and participant collapses almost immediately. A children's round at 7:30 PM precedes the adult ceremony at 8:00 PM, and the adult round is significantly more intense. The same date as Shitennōji's Doya-doya means you must choose — but Hōkaiji offers something the larger ceremony cannot: physical proximity.",
        "highlights_en": [
            "Loincloth-clad men linking arms in midwinter cold, circling in close quarters while chanting \"chōraku\" — an intimate Buddhist bare-skin ceremony with almost no tourist buffer",
            "Observer and participant barriers dissolve in a hall too small for comfortable distance — being there means being pressed against it",
            "Free admission to a ceremony unchanged since the Heian Period: the most accessible ancient weird ritual in the Kyōto calendar"
        ],
        "origin_en": "The dance is the culminating night of the Shushōe rite (January 1st–14th), which has continued at Hōkaiji since the late Heian Period. Originally a New Year's health prayer to the Yakushi Buddha, the ceremony evolved into a communal naked dance believed to physically transfer the body's impurities into the cold winter air.",
        "viewing_notes_en": "Free admission; women may attend. The grounds are extremely small — arrive well before 7:30 PM to secure a position. The nearest subway station (Higashiyama-Misasagi on the Tōzai Line) requires a 20-minute walk; bus access strongly recommended."
    },
    "fest-002": {
        "name_en": "Shitennōji Doya-doya (Shushōe Concluding Ceremony)",
        "shrine_en": "Shitennōji Temple (Rokuji Raisan Hall)",
        "prefecture_en": "Ōsaka Prefecture",
        "city_en": "Ōsaka City, Tennōji Ward",
        "date_pattern_en": "Annual, January 14th",
        "summary_en": "Shitennōji is the temple Prince Shōtoku built in 593 CE, making it among the oldest Buddhist institutions in Japan. Every January 14th, the temple marks the conclusion of its Shushōe — a 14-day New Year purification rite — with the Doya-doya, a ceremony in which hundreds of young men in white fundoshi (loincloth) and headbands scramble across the courtyard in front of the Rokuji Raisan-dō hall to seize blessed talismans (o-fuda) that have been prayed over during the rite's duration. The name \"doya-doya\" derives either from the participants' battle cries or from the Ōsaka dialect expression for \"how about that?\" — both explanations are consistent with the scene, which involves high-school-aged participants in a state of competitive physical intensity surrounded by a crowd large enough to generate its own atmospheric pressure. Currently high school students form the core of the participants, giving the ceremony a quality of youth aggression and communal chaos that is difficult to encounter in any other religious context in Japan.",
        "highlights_en": [
            "Hundreds of white-fundoshi youths in a full-contact scramble for blessed talismans in a seventh-century Buddhist courtyard — one of Ōsaka's most viscerally alive traditional spectacles",
            "The surrounding crowd's density creates a collective atmosphere that affects observers as physically as participants",
            "The simultaneous tondoyaki (New Year bonfire) in the precinct adds fire to the ceremony's already considerable energy"
        ],
        "origin_en": "The Doya-doya originates in the distribution of blessed talismans at the conclusion of Shitennōji's Shushōe rite. The talisman scramble is said to date to the early Edo Period, roughly the 17th century, though the Shushōe rite itself connects to the temple's founding in the era of Prince Shōtoku.",
        "viewing_notes_en": "Observation is free (inner precinct admission charged separately). Even on weekdays, the area around 2:00 PM is extremely crowded. Nearest station: Shitennōji-mae Yūhi-ga-oka on the Tanimachi Line (5-minute walk)."
    },
    "fest-003": {
        "name_en": "Nishinomiya Shrine Opening Ceremony — Lucky Man Race (Fukuotoko Erabi)",
        "shrine_en": "Nishinomiya Shrine (Ebisu-no-Miya Sōhonsha)",
        "prefecture_en": "Hyōgo Prefecture",
        "city_en": "Nishinomiya City",
        "date_pattern_en": "Annual, January 10th (Tōka Ebisu)",
        "summary_en": "Every year on the morning of January 10th, roughly 1,500 people who have registered in advance gather before the Akamon (Red Gate) of Nishinomiya Shrine for a ceremony that is part religious event, part 230-meter foot race, and part nationally broadcast athletic spectacle. At precisely 6:00 AM, the gate opens. The first three participants to reach the main hall become that year's Fukuotoko — the Lucky Men — whose faces and fortunes will be reported on morning news across Japan. The course is deceptively treacherous: four designated obstacles — the Tenbin Curve, the Judge's Camphor Tree, the Demon's Corner, and the Ebisu Slope — produce multiple falls annually, and the falls are the event's most reliably dramatic footage. Nishinomiya is the head shrine of Ebisu, the god of commerce and good fortune, and the belief that the first to complete the run receives an amplified portion of Ebisu's blessing each year drives participation from across the country. The ceremony captures something that few religious practices in any tradition manage: a fully sincere act of devotion conducted at a competitive sprint.",
        "highlights_en": [
            "230 meters, 1,500 competitors, a 6:00 AM gate opening — the Lucky Man Race is one of the most precisely defined ritual competitions in Japan",
            "The four obstacles produce guaranteed falls every year; the national news coverage of those falls is not incidental but central to the event's cultural function",
            "The first-place finisher's face is on national television within minutes: religious significance and public spectacle in perfect compression"
        ],
        "origin_en": "The ritual derives from Tōka Ebisu, the festival of the merchant deity Ebisu whose January 10th name day draws millions of worshippers across the Kansai region. The competitive gate-rush is said to originate in worshippers racing to make the earliest New Year prayer to the god of commerce; the current formalized format was established in the Shōwa Period.",
        "viewing_notes_en": "Observation is free. Participation requires advance registration (from approximately 10:00 PM on January 9th at Enmanji Parking Lot). Good viewing positions require arrival by 5:00 AM or earlier."
    },
    "fest-004": {
        "name_en": "Konomiya Hadaka Matsuri (Naked Men Festival — Naoi Shinto Rite)",
        "shrine_en": "Owari Ōkunitama Shrine (Konomiya)",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Inazawa City",
        "date_pattern_en": "Annual, 13th day of the 1st lunar month (approx. late Feb/early March)",
        "summary_en": "Since the year 767 CE, the Naoi Shinto rite at Konomiya has been performed without interruption — 1,250-plus years of an annual ceremony in which thousands of men strip to a white fundoshi loincloth and converge on a single individual whose touch they believe will absorb their accumulated bad fortune. The Shin-otoko (\"divine man\"), selected each year, is the ceremony's passive fulcrum: he must accept the press of thousands of bodies, must endure the ritual contact of the multitude seeking to transfer their misfortune into him, and will spend the night in a state of ritual seclusion to contain what he has absorbed. The approach procession involves men from across the Owari region — typically concentrated in the unlucky ages of 25 and 42 — surging in waves through the shrine complex, their collective motion creating a human density that first-time observers consistently describe as physically overwhelming. The additional offering of a roughly four-ton decorated rice cake and the following morning's distribution of pieces of it to supplicants frames the ceremony's double logic: purification transferred into the divine man, blessing distributed through the rice.",
        "highlights_en": [
            "Thousands of loincloth-clad men converging on a single individual to transfer their bad fortune — a ritual logic simultaneously ancient and viscerally modern",
            "The four-ton sacred rice cake offering and its morning distribution: blessing and purification operating simultaneously",
            "The Shin-otoko's ordeal — absorbing an entire community's misfortune into a single body — is one of the most demanding ritual roles in Japanese ceremonial tradition"
        ],
        "origin_en": "The rite began in 767 CE by Imperial decree during a period of epidemic illness, when a great purification (ōharae) ceremony was ordered to cleanse the nation. Over centuries, the ritual of transferring misfortune through human contact evolved from a generalized purification into the specific Shin-otoko ceremony that continues today.",
        "viewing_notes_en": "Free admission. No parking near the shrine; the nearest access point is Nagoya-tetsudō Konomiya Station (3-minute walk). Crowd density inside the precincts is extreme. Female visitors are welcome as observers."
    },
    "fest-005": {
        "name_en": "Asuka Niimasu Shrine Onda Festival (Rice Field Play)",
        "shrine_en": "Asuka Niimasu Shrine",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Asuka Village, Takaichi District",
        "date_pattern_en": "Annual, first Sunday of February",
        "summary_en": "In the Asuka Valley, where ancient Japan left more unexplained stone objects per square kilometer than anywhere else on Earth, the first Sunday of February brings a ritual that has been classified as an Important Intangible Folk Cultural Property and is consistently described as one of Japan's most direct survivals of ancient sexual cosmology in public ceremonial form. The Onda Matsuri (\"rice field play\") at Asuka Niimasu Shrine enacts the sexual union of a male and female deity as a fertility rite for the coming agricultural year, with participants in demon and Tengu masks performing a explicit ritual coupling on the stage of the main hall. Audience members scramble to catch the ritual straw sandals thrown from the stage, as possessing them is said to ensure easy childbirth. The ceremony is integrated into a day-long ritual sequence that connects ancient agricultural symbolism, Buddhist cosmology, and indigenous folk religion in a combination that has not been revised to accommodate modern sensibilities — and is, consequently, more direct and more interesting than almost anything else in the Nara religious calendar.",
        "highlights_en": [
            "A ritual explicit sexual coupling performed by masked deity figures as agricultural blessing — unchanged since the Asuka Period and unapologetic about its directness",
            "Straw sandals thrown from the stage are prized by audience members seeking easy childbirth: folk magic distributed at a public ceremony",
            "Among the most direct survivals of pre-Buddhist fertility religion in Japan's entire ceremonial landscape"
        ],
        "origin_en": "The ceremony connects to the shrine's ancient role as a rice deity sanctuary and the tradition of Dengaku (field music and ritual), which integrates sexual symbolism as the fundamental metaphor of agricultural fertility. It has been performed at this site since at least the Heian Period.",
        "viewing_notes_en": "Free admission. Advance arrival recommended. Reached from Kintetsu Kashiharajingū-mae Station by bus to the Asuka area (approx. 15 minutes)."
    },
    "fest-006": {
        "name_en": "Kamikura Shrine Otō Festival (Fire Festival of the Ascending Flames)",
        "shrine_en": "Kamikura Shrine (Kumano Hayatama Taisha subsidiary)",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Shingū City",
        "date_pattern_en": "Annual, February 6th",
        "summary_en": "Kamikura Shrine occupies the summit of a cliff above Shingū City, accessible by a steep stone staircase of 538 steps — a path considered so sacred that women were historically forbidden to ascend it. On the evening of February 6th, roughly 2,000 white-clad men carrying burning pine torches descend those 538 steps simultaneously in a human avalanche of fire. The spectacle of that many flames moving downward through darkness, the collective sound of thousands of wooden sandals on ancient stone, and the sheer physical energy of the descent combine into what observers consistently rate as the most viscerally intense festival experience in the Kumano region. The ceremony marks the first descent of the Kumano deity from the sacred summit — the theological beginning of the spring sacred season — and its combination of vertical drop, human density, and total dark illuminated only by participants' own torches creates an experience with no adequate comparison.",
        "highlights_en": [
            "2,000 torch-bearing white-clad men descending 538 stone steps simultaneously — a human river of fire that cannot be adequately conveyed in photographs",
            "The descent is not theatrical: participants are in actual physical exertion on steep ancient steps in darkness, with fire",
            "The festival marks the annual reawakening of the Kumano deity — a cosmological beginning event that has been reenacted without interruption for over a thousand years"
        ],
        "origin_en": "The Otō Festival commemorates the deity Takakuraji's descent from the sacred rock of Kamikura with a heavenly sword that aided Jinmu, Japan's legendary first Emperor, in his eastern campaign. The fire represents the deity's original descent from the mountain.",
        "viewing_notes_en": "The descent itself is restricted to registered male participants (white garb required). Observation from the base area is unrestricted and free. Shingū Station is the nearest access point. Arrive early for a good vantage from the base."
    },
    "fest-007": {
        "name_en": "Owase Yāya Festival",
        "shrine_en": "Yaotomi Shrine",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Owase City",
        "date_pattern_en": "Annual, February 1st–3rd (peak on 3rd)",
        "summary_en": "Owase is a fishing city on the Kumano coast whose Yāya Festival serves, functionally, as the local context for young men to demonstrate their worth through endurance and controlled aggression — a form of ritual initiation conducted under the sanctifying frame of the Shinto calendar. The festival's climax involves participants attempting to seize the \"Oni Gashira\" (Demon Head) — a ceremonial object that is the focus of a sustained physical competition conducted in the cold of early February. The pushing, shoving, and collision that characterize the competition are not incidental but definitional: the ceremony is explicitly a test of physical and social position, conducted in a space where aggression is temporarily authorized by ritual framing. \"Yāya\" — the festival's onomatopoeic name — derives from the shouting of the participants, a sound that has defined the city's early February acoustic environment for centuries.",
        "highlights_en": [
            "A ritual competition for a ceremonial demon head — the logic of sacred aggression in its purest local form",
            "\"Yāya\" is the sound of the participants: a festival named for the noise it makes",
            "Owase's winter fishing-port atmosphere amplifies the festival's combination of cold endurance and communal intensity"
        ],
        "origin_en": "The Yāya Festival developed over centuries as the Yaotomi Shrine's principal seasonal rite, integrating elements of young-male initiation, demon-expulsion ritual, and community social organization into a three-day event whose competitive core has remained essentially unchanged.",
        "viewing_notes_en": "Free. Owase Station on the Kisei Main Line is the nearest access point. Accommodation must be booked in advance; Owase has limited capacity."
    },
    "fest-008": {
        "name_en": "Toyohashi Oni Matsuri (Demon Festival)",
        "shrine_en": "Akumi Kambe Shinmei Shrine",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Toyohashi City",
        "date_pattern_en": "Annual, Sunday before Setsubun (approx. early February)",
        "summary_en": "On the Sunday before Setsubun (the traditional calendar's turning point between winter and spring), Toyohashi's Akumi Kambe Shinmei Shrine hosts an extraordinary festival in which a red Tengu demon — painted face, outsized papier-mâché nose, white ceremonial robes — parades through the shrine with a ceremonial bamboo pole from which hangs a large white paper streamer. The streamer is the festival's charged object: to have it touch you is to receive purification and good fortune. The demon's deliberate unpredictability in the parade, combined with the streamer's capacity to bestow blessing wherever it falls, creates a crowd dynamic of simultaneous advance and retreat — the human geometry of wanting something that may also lightly terrify you. The pairing of red Tengu and white streamer against the winter shrine backdrop produces one of the most visually striking festival images in the Tōkai region.",
        "highlights_en": [
            "A red Tengu with an outsized nose parades while dragging a purification streamer through a winter crowd — Setsubun demon-expulsion at its most theatrically realized",
            "The blessing-streamer creates a crowd dynamic of attraction and retreat: everyone wants contact, but the demon chooses its own path",
            "One of the Tōkai region's most visually striking February ceremonies — the red-and-white color contrast in a winter shrine setting is extraordinary"
        ],
        "origin_en": "The festival's demon figure represents the oni of Setsubun — Japan's traditional winter demon-expulsion ceremony — but in Toyohashi the demon has been transformed from villain to purification agent, reflecting a regional theological interpretation in which demonic energy is redirected rather than expelled.",
        "viewing_notes_en": "Free. The precise Sunday varies by year (always the Sunday before February 3rd). Toyohashi Station is accessible on the Shinkansen; local travel required from there."
    },
    "fest-009": {
        "name_en": "Suna-kake Matsuri (Sand-Throwing Festival)",
        "shrine_en": "Matsubara Shrine (Shijonawate City)",
        "prefecture_en": "Nara Prefecture / Ōsaka Prefecture",
        "city_en": "Shijonawate City (Ōsaka) / Nara area",
        "date_pattern_en": "Annual, third Sunday of February",
        "summary_en": "On the third Sunday of February, participants and observers at Matsubara Shrine engage in a ceremony that requires everyone present — regardless of what they may be wearing — to accept that sand will be thrown at them, probably repeatedly. The Suna-kake Matsuri (Sand Throwing Festival) is a purification ceremony in which throwing sand is the ritual act: the sand carried in offerings purifies everything it touches, and the throwing is both a blessing and a challenge to stand still and receive it gracefully. Those who react badly — flinching, complaining, attempting to avoid the sand — are, by the logic of the ceremony, demonstrating that the purification is working. The ceremony is one of several Japanese rituals whose logic inverts the usual relationship between comfort and blessing, and is consequently one of the more philosophically interesting entries in the category of \"bizarre festivals.\"",
        "highlights_en": [
            "Being pelted with sand is the blessing: a purification logic that inverts ordinary preferences in a physically immediate way",
            "Everyone present — participants, observers, photographers — is subject to the same ritual: there is no safe viewing position",
            "A compact, direct, and unexpectedly thoughtful entry in the category of Japanese weird festivals"
        ],
        "origin_en": "The sand-throwing ritual derives from ancient purification practices in which materials associated with the earth (sand, soil, salt) were understood to carry cleansing power. The ceremony at Matsubara Shrine has maintained this practice in a communal, participatory form that predates current documentation.",
        "viewing_notes_en": "Free. Waterproof outer layers strongly recommended. The Kintetsu Nara area provides access via local connections."
    },
    "fest-010": {
        "name_en": "Tagata Shrine Hōnen Festival (Harvest Fertility Festival)",
        "shrine_en": "Tagata Shrine",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Komaki City",
        "date_pattern_en": "Annual, March 15th",
        "summary_en": "Every year on March 15th, the Hōnen Festival at Tagata Shrine conducts what is arguably the most internationally covered Shinto ceremony in existence: the procession of a 2-meter, 60-kilogram carved wooden phallus — the shrine's principal sacred object — through the streets of Komaki on a portable shrine mikoshi, surrounded by thousands of participants and observers from around the world. The procession carries the goshintai (divine body) of the shrine's male fertility deity from the inner sanctuary to the outer shrine and back, a circuit of blessings for crop fertility, human reproduction, and the continuity of lineage that has been performed here for centuries. Sake is poured freely for the assembled crowd; phallic sweets and souvenirs are distributed and purchased; press photographers from international media take the images that will circulate globally under headlines that do not entirely capture the ritual's genuine theological context. The festival's simultaneous existence as authentic folk religion and internationally famous spectacle is, by this point, itself a cultural fact — one that the shrine navigates with evident equanimity.",
        "highlights_en": [
            "A 2-meter wooden phallus mikoshi carried through city streets by devotees seeking agricultural abundance and human fertility — ancient agricultural religion at full visible expression",
            "Free sake distribution and phallic confections for the crowd: communal celebration of the rite that has nothing transgressive within its own cultural logic",
            "BBC, CNN, and international press cover this annually — the most globally recognized Shinto ceremony, and one of the few that deserves the attention"
        ],
        "origin_en": "Tagata Shrine's fertility worship connects to the ancient Ōyashiro faith — veneration of the male creative principle as the engine of agricultural abundance and human continuity. The Hōnen Festival's procession form dates from at least the Edo Period, though the shrine's cultic tradition is substantially older.",
        "viewing_notes_en": "Free. Access via Nagoya-tetsudō Komaki Line \"Tagata-jinja-mae\" Station. Arrive early on March 15th; crowds exceed 50,000. Book accommodation months in advance."
    },
    "fest-011": {
        "name_en": "Ōagata Shrine Hōnen Festival (Feminine Fertility Ceremony)",
        "shrine_en": "Ōagata Shrine",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Inuyama City",
        "date_pattern_en": "Annual, March 15th",
        "summary_en": "On the same day and in the same geographic zone as Tagata Shrine's famous phallus procession, Ōagata Shrine conducts its complementary ceremony — a feminine fertility rite centered on the procession of a pink, peach-shaped portable shrine, with pink rice cakes distributed to the assembled crowd. The juxtaposition of the two shrines' simultaneous ceremonies on March 15th — the male principle at Tagata, the female at Ōagata, both within a short distance in northern Aichi — constitutes what scholars of Japanese folk religion have called the most concentrated surviving public expression of yin-yang fertility cosmology in the country. The Ōagata ceremony is smaller and less internationally known than Tagata's, which gives it a more local quality that is in some respects more intimate and more interesting. The pink peach symbolism connects to the Momotarō folk legend whose geographic origin is the Inuyama area, adding a layer of literary mythology to an already rich ceremonial landscape.",
        "highlights_en": [
            "The feminine counterpart to Tagata's famous rite — two complementary fertility ceremonies on the same day, 10 minutes apart, a living yin-yang cosmological pair",
            "Pink peach-shaped portable shrine and pink mochi rice cakes: the visual language of feminine fertility symbolism in a single coherent ceremony",
            "Less internationally known than Tagata and consequently more intimate — a ceremony in which the crowd-to-ritual ratio favors the ritual"
        ],
        "origin_en": "Ōagata Shrine venerates the female principle of agricultural and human fertility (the \"Ōgata\" cult) as a complementary deity to Tagata's male principle. The two shrines' ceremonies have been paired since antiquity as complementary expressions of a single cosmological worldview.",
        "viewing_notes_en": "Free. Nagoya-tetsudō Komaki Line \"Gakuden\" Station, then 15–20-minute walk. Can be combined with Tagata Shrine in a single day."
    },
    "fest-012": {
        "name_en": "Tōdaiji Shuni-e (Omizutori — The Water Drawing)",
        "shrine_en": "Tōdaiji Temple (Nigatsudō Hall)",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Nara City",
        "date_pattern_en": "Annual, March 1st–14th (torch ceremony peaks March 12th; water drawing March 13th)",
        "summary_en": "Since 752 CE, the Shuni-e ceremony at Tōdaiji has been performed every year without exception — a run of 1,270-plus consecutive years that makes it one of the longest continually held ritual sequences in human history. For fourteen days in early March, eleven monks (the Rengyōshū) enter seclusion in Nigatsudō Hall on the hillside above the Great Buddha, living in ritual isolation while performing continuous rounds of prayer, prostration, and chanting to atone for humanity's collective transgressions. The ceremony is called Omizutori (\"water drawing\") for its culminating moment on the night of March 12th–13th, when water drawn from the Wakasa Well — believed to flow from distant Wakasa Province to this sacred point — is presented as an offering. The public sees the Otaimatsu: massive pine torches, up to 8 meters long, carried along the corridor of Nigatsudō Hall and shaken over the crowd below, showering sparks that are believed to carry purification power. Catching those sparks has been an act of deliberate faith for thirteen centuries.",
        "highlights_en": [
            "1,270-plus years of annual performance without a single missed year — this is not heritage but a living obligation that the monks of Tōdaiji have honored through wars, earthquakes, and epidemics",
            "The 8-meter pine torches showering sparks over the crowd below Nigatsudō: purification delivered as fire, caught as an act of annual faith",
            "\"The true spring begins after the Omizutori\" — Nara's most ancient season-marker and the ceremony around which the year turns"
        ],
        "origin_en": "The ceremony was established in 752 CE by the monk Jitchū at the instruction of the Bodhisattva Kannon. It is classified as a jukkage (懺悔 — repentance) practice in which the monks bear the entirety of humanity's transgressions on behalf of all sentient beings.",
        "viewing_notes_en": "Torch viewing is free (Tōdaiji grounds). March 12th and weekends are most crowded. The water drawing itself (March 13th, approximately 1:30 AM) is conducted in the hall's interior. Warm clothing essential."
    },
    "fest-013": {
        "name_en": "Saga Otaimatsu (Seiryōji Temple Torch Ceremony)",
        "shrine_en": "Seiryōji Temple (Saga Shakadō)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Ukyō Ward",
        "date_pattern_en": "Annual, March 15th",
        "summary_en": "On the evening of March 15th — the same date as Tōdaiji's Shuni-e climax and Tagata/Ōagata's fertility festivals — Seiryōji Temple in Saga Arashiyama lights three massive pine torches seven meters tall in a ceremony that combines agricultural divination with Buddhist memorial. The three torches represent the three stages of the rice crop (early, middle, late), and their combustion pattern is read by the assembled priests: a fast burn on the left indicates a rich early harvest; a lingering flame on the right suggests the late crop will struggle. The ceremony enacts the Buddha's cremation — March 15th is the traditional date of Śākyamuni's death and cremation in the lunar calendar — and the agricultural divination is layered on top of that Buddhist memorial in a combination that is characteristic of the Japanese religious synthesis. The fire is large, the setting is Arashiyama's distinctive wooded valley, and the ceremony takes approximately an hour from lighting to completion.",
        "highlights_en": [
            "Agricultural fate divined by reading the burn pattern of 7-meter pine torches: a cosmological forecast delivered in fire",
            "The ceremony simultaneously commemorates the Buddha's cremation and predicts the rice harvest — a religious layering unique to Japanese syncretic tradition",
            "March 15th triple: Seiryōji torches, Tagata phallus procession, and Ōagata feminine rite all occur on the same calendar date — a logistically challenging but remarkable convergence"
        ],
        "origin_en": "The ceremony traces to the Nehan-e (涅槃会 — Nirvana Ceremony) of the lunar calendar's February 15th, marking the Buddha's parinirvana. The three torches and their agricultural divination function were integrated into the Buddhist memorial at some point in the temple's Heian-Period history.",
        "viewing_notes_en": "Free. Randen (Kyōto Tram) Arashiyama Station, then 10-minute walk. Cannot be reasonably combined with Tagata Shrine on the same day."
    },
    "fest-014": {
        "name_en": "Awashima Shrine Hina-nagashi (Doll Float Ceremony)",
        "shrine_en": "Awashima Shrine",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Wakayama City, Kada",
        "date_pattern_en": "Annual, March 3rd",
        "summary_en": "On March 3rd — Hinamatsuri, the Girls' Festival — most of Japan displays its Hina dolls on tiered shelves and eats tri-colored rice cakes. At Awashima Shrine in the fishing port of Kada, the dolls are carried to the sea and floated away. Awashima is the shrine to which Japanese families from across the country have donated unwanted Hina sets for generations: the resulting accumulation of dolls — tens of thousands of them — occupies every surface of the shrine precincts in a visual density that bypasses whimsy and enters the territory of the genuinely uncanny. On March 3rd, white-clad priests load the year's most recently donated dolls onto straw boats and push them into the sea in a ceremony that returns the dolls' accumulated feminine power and human memory to the divine realm. The image of a fleet of doll-laden boats moving slowly out into the harbor below a Wakayama winter sky is one of the most strikingly strange things the Japanese ritual calendar produces.",
        "highlights_en": [
            "Tens of thousands of Hina dolls covering every surface of the shrine grounds — an accumulation that transitions from charming to deeply uncanny at some point during the first minute of observation",
            "The ceremonial flotilla of straw boats bearing dolls into the sea: folk ritual and visual poetry simultaneously",
            "The shrine is the designated national destination for doll donations — the concentration of displaced maternal energy here has been building for generations"
        ],
        "origin_en": "Awashima Shrine venerates Sukunahikona-no-Mikoto, the deity of medicine and healing, who is associated with the protection of women's health. The practice of floating dolls (nagashi-bina) to remove human impurity was the original Hinamatsuri practice before the festival was domesticated into a display tradition.",
        "viewing_notes_en": "Free. The flotilla ceremony begins at 10:30 AM. Nankai Kada Line \"Kada Station,\" then 10-minute walk. Morning arrival recommended."
    },
    "fest-015": {
        "name_en": "Ōse Festival (Unoura Fishing Port Festival — Cross-Dressing Boat Dance)",
        "shrine_en": "Ōse Shrine",
        "prefecture_en": "Shizuoka Prefecture",
        "city_en": "Numazu City",
        "date_pattern_en": "Annual, April 4th",
        "summary_en": "At the Unoura harbor in Numazu, a group of fishermen's sons arrives on April 4th in silk kimono, elaborate wigs, white-painted faces, and women's makeup — and proceeds to dance on a decorated boat while their vessel moves through the harbor to the accompaniment of \"Chanchara okashii\" (\"how ridiculous, how absurd\") festival music. The Ōse Festival's cross-dressing dance — called Isogi Odori (brave dancing) — is a fishing-community ceremony in which young men embody feminine deities to invoke their power in the service of the year's catch. At the ceremony's peak, the boat pulls alongside the quay and the dancers leap toward the crowd, which scrambles to receive the flowers and decorations distributed from the boat. The combination of elaborate female dress, genuine skill in boat-dancing performance, and the harbor's early-spring atmosphere creates an experience with a tonal complexity that resists simple categorization.",
        "highlights_en": [
            "Young fishermen in full feminine dress dancing on a harbor boat — ritual cross-dressing as divine embodiment in the Japanese fishing tradition",
            "\"Chanchara okashii\" — the festival's own music calls its own ceremony ridiculous: a self-aware folk absurdism that makes the ceremony more rather than less interesting",
            "The harbor's physical setting and the dance's genuine skill make this more than a curiosity — it is a fully realized ceremonial form"
        ],
        "origin_en": "The festival is an offering to the Ōse shrine's female deity (possibly Ichikishimahime-no-Mikoto), in whose honor male participants take on feminine form to become vessels for her energy — a tradition of male-to-female divine embodiment widespread in coastal Japan's historical fishing communities.",
        "viewing_notes_en": "Free. The procession begins at approximately 7:30 AM; advance arrival and accommodation in Numazu recommended. Numazu Station provides access, with taxis or buses to the harbor area."
    },
    "fest-016": {
        "name_en": "Yasurai Festival (Genmushrine — Plague-Spirit Pacification)",
        "shrine_en": "Genbu Shrine (also Imamiya Shrine and Kawara-machi Shrine)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Kita Ward",
        "date_pattern_en": "Annual, second Sunday of April",
        "summary_en": "One of Kyōto's Three Great Bizarre Festivals, the Yasurai Festival takes place on the second Sunday of April — precisely the moment when the cherry blossoms are at their most restless, petals detaching and beginning to drift. In the original logic of the ceremony, this drifting was dangerous: the spirits of illness (疫神 — yamai-gami) were understood to ride on the floating blossoms, spreading sickness wherever the petals fell. The Yasurai Festival is the ceremony of persuading those spirits to stay — to settle, to be still, to remain within the flower umbrellas that are raised above the procession. The procession itself is led by figures in red, white, and yellow oni masks, carrying flower-decorated parasols and making a noise specifically designed to attract the illness spirits into the umbrella's shelter, where they can be safely contained. Passing under the flower umbrella is the ceremony's primary act of participation — sheltering under the same parasol as the captured spirits is the mechanism of protection.",
        "highlights_en": [
            "Oni-masked figures lead a procession specifically designed to attract illness demons and trap them inside flower umbrellas — a containment ceremony conducted at cherry-blossom dispersal",
            "\"Yasurai\" means \"rest, be still\": the ceremony is a direct address to spirits that the falling petals are understood to carry",
            "Passing under the flower umbrella — deliberately sheltering with the captured illness spirits — is the protection mechanism: an ancient folk logic worth understanding"
        ],
        "origin_en": "The ceremony dates to the Heian Period, when spring epidemics were attributed to malicious spirits riding on the season's dispersing flowers. \"Yasurai\" (やすらい) is the imperative form of \"yasurau\" — to rest, to be still — a direct command addressed to the illness spirits.",
        "viewing_notes_en": "Free. Nearest station: Kuramaguchi on the Karasuma Subway Line (5-minute walk). Similar ceremonies occur simultaneously at Imamiya Shrine and Kamigamo Shrine."
    },
    "fest-017": {
        "name_en": "Teryoku Fire Festival (Teryoku-o Shrine)",
        "shrine_en": "Teryoku-o Shrine",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Kakamigahara City",
        "date_pattern_en": "Annual, third Saturday of April",
        "summary_en": "On the third Saturday of April at Teryoku-o Shrine, the grounds are converted into a fire-engineering spectacle that operates at the boundary between Shinto ceremony and industrial pyrotechnics. Thousands of handheld firework devices — hi no wa (fire wheels), fixed-frame fireworks, and cascading fire fountains — are detonated simultaneously while participants carry the mikoshi portable shrine through a space where fire is falling, spinning, and erupting in every direction. The ceremony is designated an Important Intangible Folk Cultural Property by Gifu Prefecture, which implies an official recognition that what looks, from a safety standpoint, like a recipe for catastrophe is actually a precisely controlled traditional technology. \"Waterfall of fire\" and \"tunnel of fire\" are the event's descriptive landmarks; the shrine's mythology connects to Ame-no-Tajikarao, the god who opened the cave where Amaterasu had hidden, whose strength is represented by the ceremony's controlled explosion.",
        "highlights_en": [
            "A Shinto portable shrine carried through a space of simultaneously detonating handheld fireworks — fire as religious medium at its most spectacular",
            "\"Waterfall of fire\" and \"tunnel of fire\" are not metaphors but the ceremony's designated stations: architectural fireworks at point-blank range",
            "Designated an Important Intangible Folk Cultural Property — official recognition that this is a controlled tradition, not an accident waiting to happen"
        ],
        "origin_en": "The ceremony represents the mythological force of Ame-no-Tajikarao (Hand-Strength Male Deity), who hurled open the Ama-no-Iwato cave to release Amaterasu from her exile. The fire expresses that deity's overwhelming physical power.",
        "viewing_notes_en": "Free. Approximately 15 minutes by car from JR Gifu Station. Avoid synthetic fabrics — fire particles will land on clothing."
    },
    "fest-018": {
        "name_en": "Nagahama Hikiyama Festival (Children's Kabuki)",
        "shrine_en": "Nagahama Hachimangu Shrine",
        "prefecture_en": "Shiga Prefecture",
        "city_en": "Nagahama City",
        "date_pattern_en": "Annual, April 13th–16th",
        "summary_en": "The Nagahama Hikiyama Festival is a UNESCO Intangible Cultural Heritage and National Important Intangible Folk Cultural Property whose central attraction is almost certainly the most technically demanding child performance tradition in the world: boys aged 5 to 12 performing full classical Kabuki theater — with costumes, makeup, wigs, stylized vocalization, and precisely choreographed movement — on elaborately decorated floats pulled through the streets of Nagahama. Of the city's 13 hikiyama (festival floats), four are selected each year as the onstage venues, and their young performers train for months to deliver performances that, by every objective account, rival professional adult Kabuki in execution. The floats themselves are extraordinary objects of decorative craft — embroidered with Chinese brocades, carved with lacquered figures, hung with seasonal flowers — and the combination of these extraordinary stages with the extraordinary performers on them creates an experience with nothing comparable in the Japanese festival calendar.",
        "highlights_en": [
            "Children aged 5–12 performing classical Kabuki at professional standard: the most technically extraordinary child performance tradition in Japan",
            "Thirteen hikiyama floats are objects of decorative art in their own right — Chinese brocade, lacquer carving, seasonal flowers — functioning as both parade vehicles and theatrical stages",
            "Accommodation must be booked months in advance: the festival's reputation within Japan ensures full capacity across the region"
        ],
        "origin_en": "The festival is said to have originated when the feudal lord Toyotomi Hideyoshi distributed gold dust to the townspeople of Nagahama in 1575 to celebrate the birth of his son. The townspeople purchased floats and began performing on them; the children's Kabuki tradition developed through the 17th and 18th centuries.",
        "viewing_notes_en": "Float viewing is free (premium stage-side seating may be charged). JR Nagahama Station, 10-minute walk. Accommodation should be booked months in advance."
    },
    "fest-019": {
        "name_en": "Furukawa Festival — Okoshi Daiko (Rousing Drum)",
        "shrine_en": "Ketawakamiya Shrine",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Hida City",
        "date_pattern_en": "Annual, April 19th–20th",
        "summary_en": "In the preserved Edo-Period townscape of Hida Furukawa — a smaller, quieter neighbor to Takayama — the spring festival of Ketawakamiya Shrine is structured around a night ceremony that prioritizes collision over ceremony in a way that makes it unique among Japan's UNESCO-listed festival traditions. Beginning at approximately 8:30 PM on April 19th, a large oak yagura (drum tower) bearing a great taiko is shouldered by dozens of men and carried through the town's narrow streets while teams from each neighborhood attempt to physically wrestle it away from the carriers. The confrontations — the \"tsukedaiko\" encounters — are not theatrical but genuine: men are pushed, fall, collect themselves, and charge again, all in the narrow darkness of a historic street while the great drum continues to beat above the melee. The festival is simultaneously a UNESCO Intangible Cultural Heritage and the only festival in that category where physical injury is effectively a standard component of the experience.",
        "highlights_en": [
            "A UNESCO-listed festival that involves genuine physical confrontation: the \"tsukedaiko\" encounters between neighborhood teams are not staged",
            "The drum tower that serves as the festival's sacred object doubles as a mobile site of ritual combat: percussion and collision as devotion",
            "The Hida Furukawa preserved townscape provides an architectural context for the night battle that no modern festival ground could approximate"
        ],
        "origin_en": "The Okoshi Daiko originates in the Edo Period as a way of \"rousing\" the tutelary deity (ujigami) from winter sleep — the great drum's sound waking the god for the agricultural season. The competitive element emerged as neighborhood teams vied to be the group that made the first contact with the sacred drum.",
        "viewing_notes_en": "Free. JR Takayama Line \"Hida Furukawa Station,\" 5-minute walk. Accessible from Takayama but distance from Kameyama (3–4 hours) makes it a trip requiring advance planning."
    },
    "fest-020": {
        "name_en": "Spring Takayama Festival (Sannō Matsuri)",
        "shrine_en": "Hie Shrine (Sakurayama Hachiman Shrine for autumn)",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Takayama City",
        "date_pattern_en": "Annual, April 14th–15th",
        "summary_en": "The Takayama Matsuri is one of Japan's Three Great Beautiful Festivals (alongside Kyōto's Gion Festival and Chichibu Yomatsuri) and a UNESCO Intangible Cultural Heritage. The spring version (Sannō Matsuri) on April 14th–15th deploys 12 hikiyama festival floats — elaborate multi-story constructions decorated with fine lacquer, gold leaf, and intricate carvings, representing the apex of Edo Period decorative craft — through the historic merchant district of Takayama. The floats serve as stages for Karakuri Ningyo automata performances: mechanical puppets executing precisely choreographed acts driven by clockwork mechanisms concealed within the float bodies. The spring festival's most famous Karakuri is the \"Shakkyo\" lion act on the Kinryū-tai float, in which three puppets perform a sophisticated routine of coordinated movement that 18th century artisans spent years perfecting. At night, the floats are lit with 100 paper lanterns each and drawn through the dark streets in a procession that operates at an entirely different aesthetic register from the daytime ceremony.",
        "highlights_en": [
            "Twelve Edo-Period festival floats carrying mechanical puppet theaters — the most sophisticated parade-float puppet tradition in Japan",
            "The night procession of 100-lantern-lit floats through Takayama's preserved historic district: a visual experience that justifies the entire journey",
            "Book accommodation three months in advance — the festival's international fame fills every room in the region"
        ],
        "origin_en": "The Sannō Matsuri developed in the late 17th century during the era of the Kanamori clan's rule of the Hida domain. The elaborateness of the floats reflects the prosperity of Hida's timber and carpentry industry, which produced artisans capable of executing the decorative ambitions of wealthy merchants.",
        "viewing_notes_en": "Observation of float processions is free (some premium viewing seats available). JR Takayama Station from Nagoya (2 hours). Accommodation must be booked months ahead."
    },
    "fest-021": {
        "name_en": "Tado Taisha Age-Uma Shinji (Horse-Climbing Ritual, Tado Festival)",
        "shrine_en": "Tado Taisha Shrine",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Kuwana City",
        "date_pattern_en": "Annual, May 4th–5th",
        "summary_en": "On May 4th and 5th, at the foot of a 2-meter earthen ramp with a 40-degree incline, young men on horseback attempt to drive their horses up the slope in a single burst of speed. The horses that crest the top — and not all do — are read as divine oracles: the number of successful ascents, and which horses succeed, constitutes a forecast of the year's agricultural prosperity. This Age-Uma Shinji has been performed at Tado Taisha since the Nara Period and is one of Mie Prefecture's most significant shrine ceremonies, designated a Prefecture Intangible Cultural Property. In recent years, the ceremony has been subject to animal welfare concerns following injuries to horses on the steep ramp, resulting in public debate about the conditions under which traditional practices should be maintained and adapted. That debate — between cultural continuity and contemporary ethical standards — is itself a document of how Japan is navigating the pressure on living folk traditions.",
        "highlights_en": [
            "Horses climbing a 40-degree earthen ramp as divine oracles — one of Japan's most physically dramatic festival divination practices",
            "The Nara Period tradition is currently the subject of national animal welfare debate: a living ceremony confronting the ethical standards of a changed society",
            "Tado Taisha is Mie's most accessible major festival, 30 minutes from Kameyama — a short journey to one of the region's most historically dense ceremonies"
        ],
        "origin_en": "The ceremony derives from the tradition that the Tado deity descended from heaven on a white horse. Horses have been offered as living vehicles for the deity's annual descent since the Nara Period, with the ramp ascent as the divine test of which horse the deity has chosen.",
        "viewing_notes_en": "Free (parking available). Kintetsu Yōrō Line \"Tado Station,\" 20-minute walk. Approximately 30 minutes from Kameyama by car."
    },
    "fest-022": {
        "name_en": "Izawanomiya Otaue-e (Sacred Rice-Planting Ceremony)",
        "shrine_en": "Izawanomiya Shrine (Ise Jingū Geku subsidiary)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Shima City, Isobe Town",
        "date_pattern_en": "Annual, June 24th",
        "summary_en": "One of Japan's Three Great Sacred Rice-Planting Ceremonies (alongside those at Katori Shrine and Sumiyoshi Taisha), the Izawanomiya Otaue-e is a National Important Intangible Folk Cultural Property conducted on the shrine's dedicated sacred rice paddies. Young women (saotome) plant rice seedlings in the ancient hand-transplanting method while, simultaneously, a group of men called the Shinobi-otoko — naked or near-naked, their bodies representing the raw fertility force of the male principle — rush into the paddy and seize the bamboo poles bearing the sacred offerings, wrestling with each other in mud that deepens as the ritual progresses. The ceremony's logic is straightforward within ancient Japanese agricultural religion: the women provide the technical skill of cultivation; the men provide the wild energy of fertility; the combination, enacted in the presence of the shrine's deity, consecrates the season's planting. Izawanomiya is a subsidiary shrine of the Grand Shrine of Ise, giving the ceremony an unusually elevated theological context.",
        "highlights_en": [
            "Near-naked men wrestling for sacred bamboo poles in a sacred mud paddy while women plant rice seedlings: ancient Japanese agricultural cosmology at full visible expression",
            "The ceremony is subsidiary to Ise Jingū itself — a rare access point to the Grand Shrine's agricultural ritual tradition",
            "June 24th sometimes falls on a weekday — plan accordingly, as the ceremony does not adjust its calendar for tourist convenience"
        ],
        "origin_en": "Izawanomiya has served as the deity-feeding rice paddy for the Grand Shrine of Ise since before reliable historical records; references to the ceremony appear in documentation from the late Nara Period. The ceremony represents the oldest stratum of Japanese state Shinto agriculture.",
        "viewing_notes_en": "Free. Kintetsu \"Kami-no-Gō Station,\" 5-minute walk. June 24th is frequently a weekday (Wednesday in 2026) — taking time off work is recommended."
    },
    "fest-023": {
        "name_en": "Nabekaburi Festival (Pot-on-Head Festival)",
        "shrine_en": "Local shrine, Shiga Prefecture",
        "prefecture_en": "Shiga Prefecture",
        "city_en": "Shiga Prefecture (precise location varies)",
        "date_pattern_en": "Annual (date varies; check locally)",
        "summary_en": "Somewhere in the rural reaches of Shiga Prefecture, men arrive at a shrine with ceramic cooking pots balanced on their heads, proceed to conduct their prayers and offerings in this configuration, and then go home. The Nabekaburi Matsuri is the kind of small-scale folk ceremony that exists at the absolute margins of Japan's ritual documentation — too local for national media coverage, too consistent to be called an anomaly — and its logic, while peculiar to outside eyes, sits within a recognizable tradition of Japanese apotropaic (evil-repelling) practice in which physical objects placed on or around the head intercept malicious influences. The pot receives what the head should not. Whether this makes practical sense matters less than the fact that it has been enacted with apparent sincerity for a very long time by people who found it useful.",
        "highlights_en": [
            "Men attending a Shinto ceremony with ceramic cooking pots balanced on their heads — a ritual specificity that does not explain itself and does not need to",
            "One of Japan's most persistently local folk ceremonies: too small to be famous, too particular to be forgotten",
            "The apotropaic logic (the pot intercepts evil directed at the head) connects to a widespread tradition in Japanese folk religion that is rarely expressed this literally"
        ],
        "origin_en": "The ceremony derives from agricultural apotropaic (evil-averting) practice in which the cooking pot — a domestic symbol of sustenance — was used to shield the head from malicious field spirits during planting season.",
        "viewing_notes_en": "Schedule requires local verification. A small, locally organized ceremony; advance inquiry with local authorities or the shrine itself is strongly recommended. Kintetsu \"Hino Station\" provides access with taxi required."
    },
    "fest-024": {
        "name_en": "Nachi no Hifuri Shinji (Kumano Nachi Fire Festival)",
        "shrine_en": "Kumano Nachi Taisha Shrine",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Nachikatsuura Town, Higashimuro District",
        "date_pattern_en": "Annual, July 14th",
        "summary_en": "On July 14th at Kumano Nachi Taisha — the Kumano shrine whose resident deity is the Nachi Falls itself — twelve fan-shaped portable shrines (Ōgi-mikoshi) representing the twelve months of the year are carried from the main hall down the stone steps toward the base of the falls, each float accompanying a massive pine torch weighing roughly 50 kilograms and standing 6 meters tall. At the stone steps before the falls, the torches are rotated to represent the circular movement of the seasons, their flame and smoke mixing with the waterfall's mist in a combination of elemental forces whose visual intensity is difficult to overstate. This ceremony is the annual reunion of the falls deity with its main shrine — the god returning to its original form — and the torches' fire and rotation express the purification and renewal of divine energy that the reunion accomplishes. The backdrop of the 133-meter Nachi Falls behind the ceremony gives the entire event a scale that few festivals in Japan can approximate.",
        "highlights_en": [
            "Twelve 6-meter pine torches rotated before a 133-meter sacred waterfall — a fire ceremony conducted at the foot of Japan's most powerful divine presence",
            "The Ōgi-mikoshi fan-shaped portable shrines represent the twelve months returning to the deity's original body: time itself being reunited with its source",
            "July 14th is frequently a weekday — the ceremony does not accommodate its calendar to visitors, which gives it an uncommercial authenticity"
        ],
        "origin_en": "The Hifuri Shinji is the annual restoration of the Nachi Falls deity to its sacred form — the divine energy of the falls, which has been distributed across the twelve monthly shrines during the year, is reconcentrated at the falls on July 14th through the ceremonial torches' fire.",
        "viewing_notes_en": "Free. Bus from Nachikatsuura Station to \"Nachi-no-taki-mae\" stop. July 14th is often a weekday (Tuesday in 2026); accommodation in Nachikatsuura required."
    },
    "fest-025": {
        "name_en": "Toyohama Tai Festival (Giant Sea Bream Parade)",
        "shrine_en": "Local shrine, Minami-Chita area",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Minamichita Town, Chita District",
        "date_pattern_en": "Annual, late July (check locally)",
        "summary_en": "In the fishing town of Toyohama on the Chita Peninsula, the most spectacular parade object in the local summer festival is not a drum tower, not a flaming torch installation, and not a decorated float — it is a sea bream. Specifically, it is a bamboo-and-wood construction covered in white silk representing a sea bream 10 to 18 meters tall and weighing over one ton, carried through the streets by teams of young men who must coordinate the motion of an enormous sculpted fish through narrow coastal lanes. There are five such fish of varying sizes, and their procession — accompanied by the chant \"Tokoya, Toko-se!\" — culminates in the fish being carried into the sea, their return to the divine ocean completing the ceremony's logic: the fish, which comes from the sea and sustains the community, is returned to the sea as thanks. The image of a 15-meter fabric sea bream moving through a fishing village is one of the most characteristically specific images the Japanese festival calendar produces.",
        "highlights_en": [
            "A 10–18 meter cloth sea bream carried by young men through a fishing village and finally into the sea: folk pageantry at its most literally fishy",
            "The five fish vary in scale; the largest requires 50-plus carriers moving in precise coordination through narrow streets",
            "The ceremony ends in the ocean — the fish returns to where it came from: a circular devotional logic that is visually magnificent"
        ],
        "origin_en": "The festival originated in the early Edo Period as a fishing community's gratitude ceremony — the sea bream, considered the most auspicious fish in Japanese culture, is returned to the divine sea as thanksgiving for the year's catch.",
        "viewing_notes_en": "Free. Nagoya-tetsudō Kōwa Line \"Kōwa Station,\" then Umi-ko Bus to Toyohama harbor."
    },
    "fest-026": {
        "name_en": "Shiokake Festival (Seawater-Splashing Ceremony)",
        "shrine_en": "Ōshima Shrine (affiliated with Futami Okitama Shrine)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Shima City",
        "date_pattern_en": "Annual, late July (check locally)",
        "summary_en": "The ocean deity Ichikishimahime-no-Mikoto makes her annual return to the offshore island shrine of Ōshima on a day in late July, and the ceremony marking her departure from her land-side shrine involves the vigorous splashing of seawater among all participants and bystanders — a purification act that has the practical consequence of soaking everyone in the vicinity. The mikoshi (portable shrine) bearing the goddess is loaded onto a ceremonial boat; as it leaves the quay, the assembled crowd throws buckets, cups, and scoops of seawater at each other and at the departing shrine, with a thoroughness that ensures no one remains dry. The logic is ancient: seawater purifies, the purification cleanses the entire community for the year ahead, and the most effective administration of seawater is the most complete administration of seawater. Come prepared to be wet, and understand that this is the intended outcome rather than a side effect.",
        "highlights_en": [
            "An ancient purification ceremony whose primary mechanism is throwing seawater at everyone present — bring a change of clothes or embrace wetness as the point",
            "A goddess's annual ocean voyage framed as a community water fight: devotion and exuberance in the same gesture",
            "800 years of documented history make this one of the oldest surviving seawater purification festivals in the Ise-Shima region"
        ],
        "origin_en": "The ceremony commemorates an ancient tradition of sea-deity veneration in which the ocean goddess annually visited her land shrine and returned to the offshore sacred island. Seawater-purification is integral to the maritime shrine tradition of the Ise-Shima coast.",
        "viewing_notes_en": "Free (soakable clothing required). Kintetsu Ugata Station, then bus toward Wagu."
    },
    "fest-027": {
        "name_en": "Gion Festival — Yamahoko Junkō (Float Procession)",
        "shrine_en": "Yasaka Shrine",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Higashiyama Ward",
        "date_pattern_en": "Annual, July 1st–31st (float processions July 17th and 24th)",
        "summary_en": "The Gion Festival is one of Japan's Three Great Festivals, a UNESCO Intangible Cultural Heritage, and the defining event of Kyōto's summer calendar — a month-long sequence of sub-ceremonies anchored by the Yamahoko Junkō, the procession of 34 elaborately decorated yamahoko (wheeled ceremonial structures) through central Kyōto on July 17th and 24th. The floats are mobile museums of applied decorative art: the best tapestries adorning them were imported from Belgium and China in the 16th and 17th centuries and survive in better condition than contemporary equivalents in their countries of origin. The largest hoko stand 25 meters tall and weigh 12 tons; their cornering maneuver — the Tsujimawashi, executed by teams placing cut bamboo under the wheels — is itself a spectacle requiring years of training. The ceremony's origin is a 9th-century plague-prevention ritual, and the float parade has never entirely shed that function: the Naginata-boko float's young Chigo attendant, who must not touch the ground from the moment of his sacred designation through the parade's completion, remains the ceremony's charged theological center.",
        "highlights_en": [
            "34 yamahoko, the largest standing 25 meters and weighing 12 tons, carrying Belgian and Chinese tapestries from the 16th century through Kyōto's historic streets",
            "The Tsujimawashi corner turn — 12 tons of ceremonial float guided around a 90-degree turn using bamboo skids — is an engineering ritual worth watching for itself",
            "The Chigo attendant who cannot touch the ground from his sacred designation through parade completion: a child as living divine vessel, still operational in the 21st century"
        ],
        "origin_en": "The Gion Festival originated in 869 CE as the Goryō-e, a plague-appeasement ceremony in which 66 naginata (halberds) — one for each province of Japan — were erected in the Shinsen-en garden. The current float procession form developed through the Muromachi Period.",
        "viewing_notes_en": "Grandstand seating tickets (approx. ¥2,800) sell out fast; roadside viewing is free. Extreme traffic restrictions apply on procession days. Arrive early."
    },
    "fest-028": {
        "name_en": "Kyōto Gozan Okuribi (Five Mountain Send-Off Fires)",
        "shrine_en": "(Municipal ceremony — no single shrine affiliation)",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City",
        "date_pattern_en": "Annual, August 16th",
        "summary_en": "On the evening of August 16th, five mountains surrounding Kyōto are simultaneously lit with enormous bonfires in characters and shapes visible from the city below: the character for \"great\" (大) on Daimonji-yama, the characters \"Myō\" and \"Hō\" on two separate peaks, a boat shape, a second \"大\" on a mountain to the west, and a torii gate. These are the Gozan Okuribi — the Five Mountain Send-Off Fires — the annual signal that the spirits of ancestors who returned to the living world during the Obon festival are being directed back to the realm of the dead. The fires begin at 8:00 PM with the eastern Daimonji, then proceed at five-minute intervals through the remaining mountains, taking the better part of an hour to complete. The ceremony is ancient in origin, requires months of preparation, and involves sending hundreds of monks and volunteers up five separate mountains with torches before nightfall. Viewed from a rooftop bar or a hillside observation point with all five mountains in frame, the ceremony operates at an entirely different scale from ordinary fireworks.",
        "highlights_en": [
            "Five mountains simultaneously carrying giant fire-characters visible from across the city: the largest coordinated sacred signal fire in Japan",
            "The Obon ancestors, welcomed on August 13th, are sent home on August 16th — the emotional register of these fires combines gratitude, grief, and relief in a specifically Japanese configuration",
            "The 8-minute gap between each mountain's lighting creates a 40-minute ceremonial sequence in which the sky progressively fills with sacred characters"
        ],
        "origin_en": "The Gozan Okuribi's origin is debated: traditions ascribe it variously to the monk Kūkai, the monk Musō Soseki, or a simpler popular evolution from Obon observance. The five-mountain format has been in place since at least the Edo Period.",
        "viewing_notes_en": "Observation is free; premium positions require early arrival. No single spot shows all five mountains equally — choosing one or two and committing to that position is advised. Public transport only during the event."
    },
    "fest-029": {
        "name_en": "Kuwana Ishidori Festival (Japan's Loudest Festival)",
        "shrine_en": "Haiden Shrine (Kuwana)",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Kuwana City",
        "date_pattern_en": "Annual, Saturday and Sunday before August 15th",
        "summary_en": "The Kuwana Ishidori Festival has earned the self-awarded title \"Japan's Loudest Festival,\" and the award is not ironic. Approximately 40 elaborately decorated festival carts (saikuruma) carrying teams of musicians playing kane (gongs) and taiko drums at maximum continuous volume move through the streets of Kuwana in a procession whose combined sound output, during the Saturday night Shigaku (rehearsal) and the Sunday Honbiki (main procession), has been measured at levels requiring ear protection. The festival is a UNESCO Intangible Cultural Heritage; the kane-and-drum combination was specifically designed, historically, to be the loudest possible sound as an offering to the deity — the theory being that the divine receives a greater offering from a greater noise. The result is that approaching the festival from a distance involves a gradual but relentless increase in sound pressure that crosses a threshold around 300 meters from the nearest cart where \"loud\" ceases to be an adequate description.",
        "highlights_en": [
            "40 festival carts simultaneously playing gongs and drums at maximum volume: a sonic offering so intense it requires ear protection to approach safely",
            "\"Japan's Loudest Festival\" is a UNESCO Intangible Cultural Heritage — official confirmation that extreme volume can be a cultural treasure",
            "30 minutes from Kameyama: the most accessible of Mie's UNESCO festival traditions"
        ],
        "origin_en": "The Ishidori Festival began in the early Edo Period as a midsummer purification ceremony (Harae) in which clean stones were gathered from rivers and offered to the shrine. The musical procession evolved as the ceremony's central feature through the 17th and 18th centuries.",
        "viewing_notes_en": "Free. JR/Kintetsu Kuwana Station, then approximately 20-minute walk to the festival route. Ear protection recommended for close-proximity observation."
    },
    "fest-030": {
        "name_en": "Kariya Mandō Festival (Lantern Tower Balance Dance)",
        "shrine_en": "Akiba-sha Shrine (within Kariya-jō Castle precinct)",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Kariya City",
        "date_pattern_en": "Annual, last Saturday of July",
        "summary_en": "At the Akiba-sha Shrine in Kariya, young men perform what appears to be an act of balance circus but is classified as a religious ceremony: carrying bamboo-frame lantern towers 3 to 4 meters tall, fitted with burning candles, balanced on their foreheads, chins, or hands, while dancing to festival music through the shrine grounds. The Mandō (ten-thousand lantern) towers are understood as fire offerings to the fire deity Akiba Gongen — the paradox of offering fire to the god of fire protection is typical of Japanese religious logic, which tends toward concentration rather than avoidance of powerful forces. The balance dancers train their bodies for the specific physical demands of the mandō, and the combination of flame, movement, darkness, and the specific skill required to keep burning candles aloft while dancing creates an entertainment that has no equivalent in the Japanese festival calendar.",
        "highlights_en": [
            "Men dancing with 3-meter burning lantern towers balanced on their foreheads: the art form sits exactly at the intersection of devotion and acrobatics",
            "Offering fire to the god of fire-prevention — a Japanese theological logic that doubles down on potency rather than avoiding it",
            "One of the most visually distinctive of the Tōkai region's summer fire festivals"
        ],
        "origin_en": "The ceremony began in the Edo Period as a thanksgiving offering to Akiba Gongen — the fire-deity venerated particularly by townspeople fearful of urban conflagration. Offering ten-thousand lights to the fire god was understood to satisfy the deity's appetite and prevent uncontrolled burning.",
        "viewing_notes_en": "Free. JR Tōkaidō Line \"Kariya Station\" within walking distance."
    },
    "fest-031": {
        "name_en": "Ōmi Nakayama Imo-Kurabe Festival (Taro Competition Ceremony)",
        "shrine_en": "Okitama Shrine",
        "prefecture_en": "Shiga Prefecture",
        "city_en": "Hino Town, Gamo District",
        "date_pattern_en": "Annual, mid-October (check locally)",
        "summary_en": "In the agricultural heartland of Shiga Prefecture, the autumn harvest ceremony at Okitama Shrine involves participants bringing their finest taro root (satoimo) to be judged against the roots brought by their neighbors — and the outcome of that judgment is understood as a prediction of the community's prosperity for the coming year. The Imo-Kurabe (\"taro competition\") is one of Japan's most endearing bizarre festivals precisely because its mechanism is so transparent: the community's collective agricultural effort is concentrated into its most successful example, that example is presented to the deity, and the deity's evident pleasure (represented by the comparative superiority of the best taro) is taken as a favorable omen. There is no fire, no drumming, no masked procession — just very serious people assessing root vegetables against divine criteria. The specificity and straightforwardness of this arrangement is, in its own way, more interesting than many more spectacular ceremonies.",
        "highlights_en": [
            "Bringing your best taro root to a shrine to compete against neighbors' taro roots — agricultural devotion in its most direct possible form",
            "The winner's taro predicts the community's prosperity: divination through vegetable competition",
            "A small, local, entirely sincere ceremony whose lack of spectacle is precisely what makes it worth traveling to see"
        ],
        "origin_en": "The ceremony preserves ancient agricultural thanksgiving practices in which the season's finest produce was presented to the tutelary deity as evidence of the community's harvest and as a petition for continued bounty. Taro root, as a pre-rice staple in Japanese agricultural history, carries particular ceremonial weight.",
        "viewing_notes_en": "Schedule requires local verification; a small ceremony. Kintetsu \"Hino Station\" with taxi required."
    },
    "fest-032": {
        "name_en": "Ōsaka Self Festival (Seven Shrine Circuit)",
        "shrine_en": "Seven shrines in central Ōsaka",
        "prefecture_en": "Ōsaka Prefecture",
        "city_en": "Ōsaka City",
        "date_pattern_en": "Annual (date varies; check organizer's SNS)",
        "summary_en": "The \"Self Festival\" (Serufu Matsuri) is Ōsaka's contribution to the genre of contemporary participatory bizarre festival — a self-organized, cosplay-encouraged, freely improvised circuit of seven central-Ōsaka shrines that began in the 2010s among young urban residents who wanted the experience of a matsuri without the obligation of belonging to the neighborhood groups that organize traditional festivals. Participants arrive in costume (the more theatrical the better), visit the seven designated shrines in sequence, receive stamps at each, and disperse. The theological content is voluntary; the social content is the point. The festival's name — \"Self\" — reflects its founding principle: you are doing this for yourself, in the most Ōsaka-appropriate possible combination of individual energy and communal movement.",
        "highlights_en": [
            "A self-organized cosplay shrine circuit born from young Ōsakans who wanted matsuri participation without the traditional gatekeeping — a 21st-century bizarre festival origin story",
            "The seven-shrine format provides structure; everything else is negotiable: costume, company, pace, theological sincerity",
            "Ōsaka's specific combination of irreverence and genuine enthusiasm for participation makes this work in ways it probably wouldn't anywhere else"
        ],
        "origin_en": "The Self Festival emerged organically from Ōsaka's youth culture in the 2010s, drawing on the \"stamping rally\" tradition of shrine visits combined with the city's strong cosplay and subculture communities. The organizers describe it as \"traditional festival reimagined by and for modern people.\"",
        "viewing_notes_en": "Free participation. Dates and details announced via organizer's social media. No specific station requirement — the route is distributed across central Ōsaka."
    },
    "fest-033": {
        "name_en": "Uneme Festival (Court Lady Spirit Ceremony)",
        "shrine_en": "Uneme Shrine (Sarusawa Pond, Nara)",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Nara City",
        "date_pattern_en": "Annual, night of the Mid-Autumn Full Moon (approx. late September–early October)",
        "summary_en": "On the night of the mid-autumn full moon — the most beautiful moon of the Japanese year — a procession of women in Heian Period court dress leaves the Uneme Shrine at the edge of Sarusawa Pond in Nara and moves to an ornate boat moored on the water, which carries musicians performing gagaku (ancient court music) as it drifts across the moonlit pond. The ceremony commemorates an uneme — a court serving woman — who is said to have drowned herself in Sarusawa Pond after the Emperor's affections withdrew from her: a story of imperial abandonment and feminine grief that has been commemorated by this ceremony since the 8th century. The moon's reflection in the pond, the sound of gagaku across the water, and the procession of historical court dress create an atmosphere of concentrated historical pathos that operates in a register most festivals cannot reach.",
        "highlights_en": [
            "A boat carrying gagaku musicians drifting across a moon-reflecting pond in the night: a ceremonial aesthetic that has not been updated since the Heian Period and does not need to be",
            "The ceremony has commemorated a court lady's drowning suicide for over 1,200 years — grief encoded in ritual form",
            "The mid-autumn full moon as the ceremony's specific temporal trigger: the entire ceremony is designed around the moon's reflection on the pond"
        ],
        "origin_en": "The ceremony dates to the late 8th century CE and is associated with the tradition that an uneme (court serving woman) drowned in Sarusawa Pond after being abandoned by the Emperor. The ritual boat and gagaku music were established as perpetual memorial for the displaced court woman.",
        "viewing_notes_en": "Free. The night of the lunar August 15th (approximately early–mid October in the solar calendar; 2026 date approximately October 2nd). Nara City center, near Kōfukuji Temple."
    },
    "fest-034": {
        "name_en": "Kurama Fire Festival (Yuki Shrine Shinko-sai)",
        "shrine_en": "Yuki Shrine",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Sakyō Ward (Kurama)",
        "date_pattern_en": "Annual, October 22nd",
        "summary_en": "On the night of October 22nd, the mountain village of Kurama north of Kyōto becomes the setting for one of Kyōto's Three Great Bizarre Festivals: a fire procession in which the entire community participates, carrying torches from sunset through midnight in a progression that moves from children's small fires to the great pine torches of adult men, and finally to the deity's procession through the illuminated dark. The shouted invocation \"Saireya, Sairyō!\" has echoed through Kurama's narrow mountain street since 940 CE — the year the ceremony was established to welcome the deity Yuki Myōjin's relocation from the Imperial Palace to this mountain village. The celebration of that arrival has been staged every year since, making it one of Kyōto's oldest annual events. The festival takes place on the same date as the Jidai Matsuri procession in central Kyōto, requiring visitors to choose; those who choose Kurama consistently report that the choice was correct.",
        "highlights_en": [
            "\"Saireya, Sairyō!\" — a war cry that has been shouted in this mountain village on October 22nd for over 1,000 years, without modification",
            "The progression from children's torches to the great pine torches of adult men to the deity's procession maps the entire community's participation across a single night",
            "Kurama's narrow mountain street lit by hundreds of torches is an image the 21st century has not been able to improve upon"
        ],
        "origin_en": "In 940 CE (Tengyō 3), during a period of civil war, the deity Yuki Myōjin was transferred from the Imperial Palace to Kurama as a protective measure. The villagers greeted the deity's arrival with torches; the greeting has been re-enacted every October 22nd since.",
        "viewing_notes_en": "Free. Traffic restrictions from 3 PM; Eizan Electric Railway \"Kurama Station\" is the only practical access. The return journey after the ceremony is extremely crowded."
    },
    "fest-035": {
        "name_en": "Nada Kenka Matsuri (Fighting Festival)",
        "shrine_en": "Matsubara Hachiman Shrine",
        "prefecture_en": "Hyōgo Prefecture",
        "city_en": "Himeji City",
        "date_pattern_en": "Annual, October 14th–15th",
        "summary_en": "The Nada Kenka Matsuri is one of Japan's Three Great Fighting Festivals, and the description is accurate: three portable shrines (mikoshi) are carried by competing neighborhood teams who then deliberately crash the shrines against each other with sufficient force to break them. The operating rule — \"you may damage your body, but you must not damage the shrine\" — creates a form of competitive devotion that channels human aggression into the service of purification: the damage the shrines absorb represents the community's accumulated bad fortune, physically beaten out of them. The carriers wear happi coats, traditional headbands, and an expression of concentrated ferocity; the crashes between mikoshi send splinters flying and occasionally send carriers to the ground. By the ceremony's end, the shrines are visibly damaged. This is not an accident but the entire point.",
        "highlights_en": [
            "Three portable shrines deliberately crashed against each other until they break: the logic of purification through structural sacrifice",
            "\"Damage your body, not the shrine\" — a rule that produces a devotional aggression with no equivalent in any other festival tradition",
            "One of Japan's Three Great Fighting Festivals, and the one where the shrines themselves bear the community's misfortune most literally"
        ],
        "origin_en": "The festival dates to the early Edo Period. The theological basis is the belief that violent contact between the mikoshi transfers the impurities and bad fortune of the carriers and the community into the shrine's structure, which is then ritually cleaned and repaired — absorbing and neutralizing the accumulated negative energy.",
        "viewing_notes_en": "Free. JR San-yō Line \"Shirahama-no-Miya Station,\" 5-minute walk."
    },
    "fest-036": {
        "name_en": "Nibu Festival (Laughing Festival)",
        "shrine_en": "Nibu Tsuhime Shrine",
        "prefecture_en": "Wakayama Prefecture",
        "city_en": "Katsuragi Town, Ito District",
        "date_pattern_en": "Annual, November 3rd",
        "summary_en": "At the Nibu Tsuhime Shrine in the mountains of Wakayama Prefecture, a herald painted entirely white — face, neck, hands — in a garish costume of red, yellow, and blue, with the character for \"laugh\" written on one cheek and a torii gate drawn on the chin, processes through the village ringing a bell and shouting \"E, tanoshi-ya! Yo wa raku-ja, Warae, warae, Wahhahhā!\" — roughly: \"Rejoice! Life is easy! Laugh, laugh, Hahaha!\" — demanding that everyone he encounters respond in kind. The Nibu Matsuri (also called the \"Warai Matsuri,\" the Laughing Festival) is a Wakayama Prefecture Intangible Cultural Property and one of Japan's most direct surviving examples of obligatory ritual laughter — laughter that is not a response to humor but a ceremonial act, the collective exorcism of sorrow and stagnation through the physical mechanism of the laughing body.",
        "highlights_en": [
            "A herald painted white with \"laugh\" written on his cheek demands that every person he encounters laugh out loud — obligatory ceremonial laughter as a folk purification technology",
            "The festival's mythology traces to a deity who arrived late to the divine assembly and was cheered up by her community's laughter: communal care encoded as annual ceremony",
            "Wakayama's mountainous isolation has preserved ceremonies like this in forms that more accessible areas have lost — this is living folk religion at the margin"
        ],
        "origin_en": "The ceremony commemorates the legend that the shrine's deity, Nibu Tsuhime, arrived late to the divine assembly at Izumo (the annual gathering of all Japan's deities) because she had made a mistake — and that the villagers consoled her grief with laughter. The annual ceremony re-enacts that consolation.",
        "viewing_notes_en": "Free. JR Kisei Main Line \"Wasa Station,\" then approximately 10 minutes by taxi."
    },
    "fest-037": {
        "name_en": "Hida Takayama Autumn Festival (Hachiman Matsuri)",
        "shrine_en": "Sakurayama Hachiman Shrine",
        "prefecture_en": "Gifu Prefecture",
        "city_en": "Takayama City",
        "date_pattern_en": "Annual, October 9th–10th",
        "summary_en": "The autumn counterpart to the spring Sannō Matsuri, the Hachiman Matsuri on October 9th–10th deploys a different set of nine hikiyama floats through Takayama's preserved Edo townscape — the same architectural tradition, the same mechanical puppet theaters, the same technical mastery, but with autumn foliage replacing spring blossoms as the backdrop and a night procession that many visitors rate as the more beautiful of the two events. The festival floats are lit by lanterns (100 per float) and pulled through streets whose merchant-district architecture has survived essentially intact since the Edo Period; the combination of historical street, historical float, and historical puppet theater produces an experience of concentrated temporal density that modern Japan provides almost nowhere else. The Karakuri automata of the autumn festival include some different and notably complex performances from the spring festival; comparing them is an excuse for visiting Takayama twice in the same year.",
        "highlights_en": [
            "Nine hikiyama floats lit by 100 lanterns each, moving through Edo-Period streets in the dark: the night procession's beauty exceeds what any description can convey",
            "The autumn foliage backdrop transforms the already spectacular spring-festival visual into something with a different, more melancholy register",
            "Comparing the spring and autumn Karakuri puppet performances is a legitimate reason to visit Takayama in both April and October"
        ],
        "origin_en": "The Hachiman Matsuri developed in the mid-Edo Period as the autumn festival of Sakurayama Hachiman Shrine. It uses a separate set of floats from the spring festival, reflecting the economic competition between Takayama's two shrine districts.",
        "viewing_notes_en": "Free (premium seating available). JR Takayama Station from Nagoya (2 hours). Accommodation must be booked months in advance, especially for the nights of October 9th–10th."
    },
    "fest-038": {
        "name_en": "Kōryūji Ushi Matsuri (Ox Festival at Uzumasa)",
        "shrine_en": "Kōryūji Temple",
        "prefecture_en": "Kyōto Prefecture",
        "city_en": "Kyōto City, Ukyō Ward",
        "date_pattern_en": "Irregular (currently suspended — verify status before planning)",
        "summary_en": "The Kōryūji Ushi Matsuri is one of Kyōto's Three Great Bizarre Festivals — and the one that operates on an irregular schedule that has included multi-year suspensions, making it either the rarest or the least reliable of the three depending on your perspective. When it occurs, the ceremony involves a figure wearing the sacred mask of Matarajin — a deity of esoteric Buddhism associated with the Tendai school, whose identity and origin remain genuinely mysterious — riding an ox through the darkened precincts of Kōryūji Temple accompanied by four attendants in demon masks. Three circuits of the precinct, followed by the reading of a sacred sutra, complete the ceremony, during which audience members are encouraged to heckle the proceedings — an instruction that transforms what would otherwise be a solemn ritual into something stranger and more alive. Kōryūji was founded by the Hata clan, immigrant artisans from the Korean Peninsula, whose specific theological inheritance accounts for several unusual features of the temple's ritual tradition.",
        "highlights_en": [
            "A masked ox-mounted deity and four demon attendants circuit a darkened temple in a ceremony whose audience is specifically encouraged to heckle — a Tantric ritual that breaks its own fourth wall",
            "Matarajin's identity and origin are genuinely debated by religious historians: a deity whose cult contains unsolved theological puzzles",
            "The irregular schedule makes attending a matter of timing and attention — which is consistent with the ceremony's character"
        ],
        "origin_en": "The ceremony is associated with the Hata clan, immigrant artisans who founded Kōryūji in the 7th century, and with the cult of Matarajin — a protective deity of Tantric Buddhist esoteric practice whose precise origins are contested between Indian, Chinese, and Korean sources.",
        "viewing_notes_en": "Currently irregular; confirm status with the temple before traveling. When held: Randen (Kyōto Tram) \"Uzumasa Kōryūji Station,\" immediately adjacent."
    },
    "fest-039": {
        "name_en": "Okuyama Gongen Mushi-okuri (Insect-Sending Ceremony)",
        "shrine_en": "Okuyama Daigongen",
        "prefecture_en": "Shizuoka Prefecture",
        "city_en": "Hamamatsu City, Okuyama area",
        "date_pattern_en": "Annual (date varies; check locally)",
        "summary_en": "The Mushi-okuri is an agricultural folk ritual in which the insects that damage rice crops are ceremonially \"sent\" to the local shrine — not killed, not repelled, but honored and removed. Participants carry torches and lanterns around the edges of their rice paddies in a procession that is understood to invite the insects to follow the lights to a new location, sparing the crops without the violence of extermination. The ceremony is a survival of an ancient animistic worldview in which insects inhabit spirits, and spirits can be negotiated with rather than simply destroyed. At Okuyama in Hamamatsu, the ceremony has merged with the area's famous firefly season, giving the Mushi-okuri the additional function of a firefly-appreciation event whose spiritual basis makes it more than a summer nature walk.",
        "highlights_en": [
            "Insects are ceremonially invited to follow torches away from the rice paddies — agricultural pest management conducted through spiritual negotiation rather than extermination",
            "The animistic worldview that considers insects as spirit-bearing beings, addressable through ceremony, is preserved here in living practice",
            "The firefly season overlay transforms a pest-management ceremony into one of Shizuoka's most atmospherically distinctive summer events"
        ],
        "origin_en": "Mushi-okuri ceremonies derive from ancient Japanese animist agricultural practice in which the spirits inhabiting pest insects were understood to be responsive to ceremonial invitation. The practice was widespread across Japan's rice-farming regions; Okuyama preserves one of the more intact surviving forms.",
        "viewing_notes_en": "Local schedule confirmation required. A small, community-organized ceremony."
    },
    "fest-040": {
        "name_en": "Mie Tomida Whale Ship Festival (Toride Shrine)",
        "shrine_en": "Toride Shrine",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Yokkaichi City",
        "date_pattern_en": "Annual, mid-October (check locally)",
        "summary_en": "In the former whaling communities of Ise Bay, the memory of cetacean hunting — an industry that shaped the culture, the diet, and the self-image of Japan's Pacific coast communities for centuries — survives in the Kujira-bune Matsuri (Whale Ship Festival) at Toride Shrine in Tomida. Men carry elaborate festival floats constructed to resemble whales — bamboo frames covered in white fabric, built to scale — through the streets in a performance that reenacts the drama of the whale hunt: the approach, the harpooning, the struggle, the catch. The floats are a designation of Mie Prefecture as an Intangible Cultural Property. In an era when the ethics of whale hunting have become a global point of contention, the Tomida ceremony occupies an unusual position: a preservation of a working-community relationship with a specific marine animal, encoded in festival form for a world in which that relationship has become impossible to continue.",
        "highlights_en": [
            "Bamboo-and-fabric whale floats carried through streets reenacting the hunt: an extinct industry's memory preserved in festival performance",
            "The ceremony connects to centuries of Ise Bay coastal culture in which the whale was both economic necessity and spiritual presence",
            "30 minutes from Kameyama: one of the region's most culturally specific and least-visited festival traditions"
        ],
        "origin_en": "The festival began in the Edo Period among fishing and whaling communities of Ise Bay as a thanksgiving and prayer ceremony. The whale-shaped floats represent gratitude to the whales whose bodies sustained the community and a prayer for the annual return of the pods.",
        "viewing_notes_en": "Free. JR Kansai Main Line \"Tomida Station\" vicinity. Approximately 30 minutes from Kameyama by car."
    },
    "fest-041": {
        "name_en": "Isonokami Shrine Chinkon-sai (Soul-Vivification Ceremony)",
        "shrine_en": "Isonokami Jingū",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Tenri City",
        "date_pattern_en": "Annual, November (date varies; check shrine)",
        "summary_en": "Isonokami Jingū is one of Japan's oldest shrines — built before the current Nara city and possibly before the concept of an imperial capital existed — and it holds, in its inner sanctuary, a divine sword (Futsunomitama-no-Tsurugi) understood to be one of the most powerful sacred objects in the Japanese cosmological tradition. The Chinkon-sai (\"soul vivification ceremony\") is performed here around the time of the winter solstice, when the souls of living people are understood to wane alongside the diminishing sunlight. Shaking a sacred sword near an altar — the ancient gesture of tamafuri (soul-shaking) — is the mechanism by which the soul's energy is re-intensified, restoring vitality for the coming year. Witnessing a ceremony at Isonokami, with roosters still walking freely through the shrine precinct in a tradition that dates to the Nara Period, produces a sense of temporal displacement that few other functioning sacred sites can match.",
        "highlights_en": [
            "The ritual mechanism is literally sword-shaking to re-energize the human soul before winter — an ancient therapeutic cosmology conducted with a National Treasure blade",
            "Roosters roam free through the shrine precincts as they have for 1,300 years: the most tangible evidence of the Nara Period you can encounter in modern Japan",
            "One of Japan's oldest shrines performing one of its oldest ceremonies at the winter solstice — temporal compression of rare intensity"
        ],
        "origin_en": "The Chinkon-sai connects to the Mononobe clan's tradition as guardians of the imperial weapons treasury. The ceremony's tamafuri (soul-shaking) ritual is the oldest documented form of Japanese soul-maintenance practice, predating Buddhism and connected to the pre-Buddhist understanding of the soul as a vibrating living energy.",
        "viewing_notes_en": "General access to the shrine is free; some ceremonial events are internal. JR Sakurai Line \"Tenri Station,\" then bus or taxi."
    },
    "fest-042": {
        "name_en": "Nagahama Tsuyamono Festival (Autumn Splendor Ceremony)",
        "shrine_en": "Nagahama Hachimangu Shrine",
        "prefecture_en": "Shiga Prefecture",
        "city_en": "Nagahama City",
        "date_pattern_en": "Annual, mid-October (date varies; check shrine)",
        "summary_en": "In the castle-town of Nagahama, whose Hikiyama Festival in April is one of Japan's most celebrated UNESCO heritage events, the autumn calendar includes a harvest-thanksgiving ceremony centered on the display of \"tsuyamono\" — glossy, lustrous, beautiful objects — as offerings to the shrine's deity. The term tsuyamono (艶物) carries connotations of both physical luster and erotic attractiveness; the ceremony's original understanding of beauty as a form of divine currency — offering the most visually compelling things available as appreciation for the year's harvest — reflects a theological aestheticism that is characteristic of the Nagahama area's Toyotomi Hideyoshi connection. The ceremony operates in a quieter register than the Hikiyama Festival but rewards visitors who seek the autumnal, non-spectacular version of Nagahama's cultural depth.",
        "highlights_en": [
            "\"Tsuyamono\" — lustrous, beautiful objects — offered to a deity as the aesthetic equivalent of harvest thanks: theology as appreciation for beauty",
            "Nagahama in October combines the Hachiman Matsuri atmosphere with fall foliage in a setting whose Edo-Period merchant-town character is better preserved than almost anywhere in Shiga",
            "A quieter, more contemplative festival experience than the famous April events — Nagahama in autumn for those who have already done it in spring"
        ],
        "origin_en": "The autumn ceremony at Nagahama Hachiman Shrine traces to the Toyotomi Hideyoshi era of the 16th century, when Nagahama was a prosperous castle town and its merchants developed a tradition of offering their most luxurious goods to the shrine as harvest gifts.",
        "viewing_notes_en": "Check schedule with Nagahama Hachimangu Shrine. JR Nagahama Station, 10-minute walk."
    },
    "fest-043": {
        "name_en": "Toyohashi Donki Festival (Fox, Tengu, and Child-Chasing Rite)",
        "shrine_en": "Chōshōji Temple (Inari deity)",
        "prefecture_en": "Aichi Prefecture",
        "city_en": "Toyohashi City",
        "date_pattern_en": "Annual, early December (check locally)",
        "summary_en": "In the temple grounds of Chōshōji in Toyohashi, three supernatural entities — a white fox, a red Tengu, and a blue Tengu — emerge to chase children through the precincts. Contact with these figures (running away is permitted, even recommended) transfers purification to the child and expels the misfortune of the year. The spectacle — small children being pursued by a white-faced fox figure and two dramatically costumed Tengu demons through a small temple compound — operates at a register that is simultaneously frightening and joyful, and the children who receive the touching experience what the ceremony has always promised: that fear, properly framed and ritually contained, is a form of growth. The Donki Matsuri is classified as a local folk ceremony of the Nagoya region and remains genuinely little-known outside Toyohashi.",
        "highlights_en": [
            "Children being chased through temple grounds by a white fox and two Tengu demons: ritual fear as purification delivery system",
            "The theological logic — contact with the supernatural as the mechanism of annual cleansing — has remained unchanged since the ceremony's Edo Period origins",
            "One of the Tōkai region's most genuinely obscure folk ceremonies: the lack of tourist infrastructure is part of the attraction"
        ],
        "origin_en": "The ceremony derives from the Inari fox and Tengu cult associated with the temple's guardian deities. Winter exorcism through supernatural encounter is a traditional Japanese therapeutic practice in which controlled fear clears the body of accumulated spiritual debris.",
        "viewing_notes_en": "Free. Nagoya-tetsudō Main Line \"Kokufu Station\" vicinity."
    },
    "fest-044": {
        "name_en": "Kasuga Wakamiya On-matsuri (The Unbroken Festival)",
        "shrine_en": "Kasuga Taisha (Wakamiya Shrine subsidiary)",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Nara City",
        "date_pattern_en": "Annual, December 17th (main procession); ceremonies extend December 15th–18th",
        "summary_en": "The Kasuga Wakamiya On-matsuri has been performed every year since 1136 CE — 890-plus consecutive years — which qualifies it as one of the longest continuously held festival events in human history. The ceremony's theological purpose is to comfort the Wakamiya deity (a child-deity of Kasuga Taisha, Japan's great Fujiwara clan shrine) through performances of the arts — ancient court music, Noh theater, Kagura dance, Sarugaku comedy — that the deity is understood to enjoy. The procession on December 17th deploys hundreds of participants in period costumes from the Heian through Edo eras in a sequence that constitutes a full historical panorama of Japanese court and warrior dress. The ceremony's climax, the Otabisho rite conducted at the temporary shrine in the Shiba area from 2:00 PM, is the deity's own performance review of the day's offerings. A third ceremony — the Ochakai (tea ceremony) — and the midnight Senko-no-Gi (ceremonial lighting) round out an event whose full duration spans four days.",
        "highlights_en": [
            "890-plus consecutive years without missing a single annual performance: the most durably uninterrupted festival in Japan and one of the longest in the world",
            "A deity comforted by court music, Noh, and comedy: the theological premise that arts are the highest form of divine offering",
            "The midnight Senko-no-Gi torch-lighting ceremony, conducted in total darkness at the temporary shrine, is the most atmospherically charged moment in Nara's entire festival calendar"
        ],
        "origin_en": "The On-matsuri was established in 1136 CE by the Imperial Regent Fujiwara Tadamichi to pray for the relief of famine and plague. It has been performed every year since — through civil wars, epidemics, and natural disasters — as a formal obligation of the Kasuga institution to the Wakamiya deity.",
        "viewing_notes_en": "The Otabisho procession and Noh performances are free to observe. December 17th afternoon in Nara is very crowded. The midnight Senko ceremony requires attendance in darkness; bring a flashlight."
    },
    "fest-045": {
        "name_en": "Suzuka Mito Shinji (Year-End Ceremony at Tsubaki Grand Shrine)",
        "shrine_en": "Tsubaki Grand Shrine",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Suzuka City",
        "date_pattern_en": "Annual, late December (check shrine for exact date)",
        "summary_en": "At the national head shrine of Sarutahiko-no-Ōkami in Suzuka, the year's final major ceremony is an austere, formalized reporting to the deity of the year's events — a divine debriefing in which the chief priest, in ancient court dress, presents an account of the year's ceremonies, offerings, and the general state of the nation to the shrine's deity, who is understood to receive this information before the year closes. The ceremony's character reflects Tsubaki Shrine's role as a path-opening shrine (michi-biraki): it is not a celebration but a formal close, a completion of the annual ritual cycle in the presence of the deity who guides transitions and crossroads. For visitors familiar with Tsubaki's spring and summer ceremonies, this year-end ceremony provides a contemplative counterpoint that reveals the shrine's ceremonial depth.",
        "highlights_en": [
            "A formal year-end report to a deity — the divine accounting of the annual cycle, presented in ancient court dress",
            "Tsubaki Shrine's role as a crossroads and path-opening deity gives the year-end ceremony a specifically transitional character",
            "30 minutes from Kameyama: Tsubaki's full ceremonial calendar is accessible as a local annual circuit"
        ],
        "origin_en": "The Mito Shinji connects to the ancient practice of nenkan-houkoku (annual divine report) — the tradition in which shrine priests formally communicate the year's events to the resident deity before the year closes. At Tsubaki, the ceremony's format reflects the shrine's proximity to the Ise Jingū ceremonial tradition.",
        "viewing_notes_en": "Exact date requires confirmation with Tsubaki Grand Shrine. Accessible from Kameyama IC by car in approximately 30 minutes."
    },
    "fest-046": {
        "name_en": "Isonokami Shrine New Year Ceremony (Birth Cry Festival)",
        "shrine_en": "Isonokami Jingū",
        "prefecture_en": "Nara Prefecture",
        "city_en": "Tenri City",
        "date_pattern_en": "Annual, January 1st",
        "summary_en": "Japan's oldest shrine — Isonokami Jingū, whose founding predates the Imperial capital at Nara — greets the New Year with a ceremony unique in the Japanese ceremonial calendar: the Ubugoe-sai (Birth Cry Festival), in which the sounds of new life are presented to the shrine's divine sword as an offering of vitality for the coming year. The free-roaming roosters that have occupied the shrine precincts since the Nara Period are the ceremony's living participants: their crowing at dawn constitutes the original \"birth cry\" (ubugoe) offered to the ancient sword deity to inaugurate the year. The resulting New Year atmosphere at Isonokami — ancient shrine, dawn darkness, free-ranging birds, a sword whose power the ceremony is invoking — has no equivalent in the Yamato region.",
        "highlights_en": [
            "A sacred sword receives the cries of newborn life as its New Year offering — a theological specificity that rewards time spent understanding it",
            "Roosters roaming the shrine grounds as they have for 1,300 years, crowing at dawn as the ceremony's primary participants",
            "Japan's oldest shrine on New Year's dawn: the most temporally compressed moment in the Yamato region's annual ceremonial calendar"
        ],
        "origin_en": "The ceremony connects to the Mononobe clan's ancient tradition of offering the first sounds of the new year to their guardian sword deity. The roosters' connection to the Isonokami tradition relates to the ancient Japanese identification of the rooster's dawn cry with the sun's revival — the cry that ends darkness.",
        "viewing_notes_en": "Free. Extremely crowded on January 1st morning. JR Sakurai Line \"Tenri Station,\" then bus or taxi. Arrive before dawn for the full ceremonial atmosphere."
    },
    "fest-047": {
        "name_en": "Tado Taisha New Year Horse Race (New Year Shinto Rite)",
        "shrine_en": "Tado Taisha Shrine",
        "prefecture_en": "Mie Prefecture",
        "city_en": "Kuwana City",
        "date_pattern_en": "Annual, January 1st–3rd",
        "summary_en": "Tado Taisha — Mie Prefecture's largest New Year destination, drawing hundreds of thousands of visitors over the first three days of January — pairs its popular first-visit (hatsumōde) with the Gantan Uma Kake: a New Year horse race in which sacred horses (shinme) gallop through the shrine grounds as a divination of the coming year's prospects. The ritual connects directly to the shrine's founding mythology, in which the great deity Tado-no-Kami descended from the heavens on a white horse — so each year's race is a re-enactment of arrival, an annual re-commissioning of divine presence. The race is a calmer and more solemn counterpart to the shrine's famous May Agemba rite (the horse-climbing ceremony), offering a quieter but no less meaningful encounter with Tado's defining equine symbolism.",
        "highlights_en": [
            "Sacred horses galloping through the shrine grounds as a New Year divination — the divine arrival re-enacted annually",
            "The largest New Year pilgrimage destination in Mie Prefecture: the atmosphere of hundreds of thousands sharing a sacred space",
            "A counterpart to the famous May Agemba ceremony: the same equine symbolism in its quietest, most solemn register"
        ],
        "origin_en": "The New Year horse rite connects to Tado's founding legend of a deity descending on a white horse. Annual horse ceremonies at Tado are believed to date to the Nara Period, when the shrine was established as a major cultic center of the Yamato state.",
        "viewing_notes_en": "Free. Extremely crowded January 1st–3rd. Kintetsu Yōrō Line 'Tado Station,' then 20-minute walk. Parking available but congested during the New Year period."
    }
}

# ─────────────────────────────────────────────
# MERGE FUNCTION
# ─────────────────────────────────────────────

def merge_spots():
    with open('/home/user/workspace/chinspot-map/spots.json', 'r', encoding='utf-8') as f:
        spots = json.load(f)
    
    result = []
    for spot in spots:
        sid = spot['id']
        merged = copy.deepcopy(spot)
        if sid in SPOTS_EN:
            en = SPOTS_EN[sid]
            merged['name_en'] = en.get('name_en', '')
            merged['prefecture_en'] = en.get('prefecture_en', '')
            merged['city_en'] = en.get('city_en', '')
            merged['summary_en'] = en.get('summary_en', '')
            merged['highlights_en'] = en.get('highlights_en', [])
        result.append(merged)
    
    with open('/home/user/workspace/chinspot-map/spots_en.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"spots_en.json: {len(result)} entries written")
    return result

def merge_festivals():
    with open('/home/user/workspace/chinspot-map/festivals.json', 'r', encoding='utf-8') as f:
        festivals = json.load(f)
    
    result = []
    for fest in festivals:
        fid = fest['id']
        merged = copy.deepcopy(fest)
        if fid in FESTIVALS_EN:
            en = FESTIVALS_EN[fid]
            merged['name_en'] = en.get('name_en', '')
            merged['shrine_en'] = en.get('shrine_en', '')
            merged['prefecture_en'] = en.get('prefecture_en', '')
            merged['city_en'] = en.get('city_en', '')
            merged['date_pattern_en'] = en.get('date_pattern_en', '')
            merged['summary_en'] = en.get('summary_en', '')
            merged['highlights_en'] = en.get('highlights_en', [])
            merged['origin_en'] = en.get('origin_en', '')
            merged['viewing_notes_en'] = en.get('viewing_notes_en', '')
        result.append(merged)
    
    with open('/home/user/workspace/chinspot-map/festivals_en.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"festivals_en.json: {len(result)} entries written")
    return result

if __name__ == '__main__':
    import json
    import copy
    merge_spots()
    merge_festivals()
    print("Done.")
