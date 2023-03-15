from utils.config.emojis import Emojis
from utils.config.roles import Roles


class BotLinks:
    template_server = "https://discord.gg/xQs94q4bvE"
    support_server = "https://discord.gg/cT9rmtf"

    breadwinner_invite = "https://discord.com/oauth2/authorize?client_id=730594098695635014&permissions=314432&scope=bot%20applications.commands"

    roblox_group = "https://www.roblox.com/groups/9861497/Bread-Winner-V2#!/about"
    roblox_group_store = "https://www.roblox.com/groups/9861497/Bread-Winner-V2#!/store"

    youtube_channel = ("https://www.youtube.com/channel/UCQY8Yq4RXRdThDbKyLGmTtA",)
    signing_video = "https://youtu.be/GIic9B7QIXQ"

    topgg = "https://top.gg/bot/730594098695635014"
    topgg_vote = "https://top.gg/bot/730594098695635014/vote"


class Colors:
    tan = 0xECDEC1
    brown = 0x693C1E
    red = 0xC15B4E
    white = 0xFFFFFF


class Images:
    check_mark = "https://cdn.discordapp.com/emojis/884442474855170059.png"


class EmojisDict:
    # NFL
    NFL_EMOJIS = dict(zip(Roles.nfl, Emojis.nfl))
    NFL_NEON_EMOJIS = dict(zip(Roles.nfl, Emojis.nfl_neon))
    NFL_NEON2_EMOJIS = dict(zip(Roles.nfl, Emojis.nfl_neon2))
    NFL_HELMET_EMOJIS = dict(zip(Roles.nfl, Emojis.nfl_helmet))
    NFL_3D_EMOJIS = dict(zip(Roles.nfl, Emojis.nfl_3d))
    NFL_LOGOS_EMOJIS = dict(zip(Roles.nfl_logos, Emojis.nfl_logos))
    # NBA
    NBA_EMOJIS = dict(zip(Roles.nba, Emojis.nba))
    NBA_LOGOS_EMOJIS = dict(zip(Roles.nba_logos, Emojis.nba_logos))
    # MLB
    MLB_EMOJIS = dict(zip(Roles.mlb, Emojis.mlb))
    MLB_LOGOS_EMOJIS = dict(zip(Roles.mlb_logos, Emojis.mlb_logos))
    # NHL
    NHL_EMOJIS = dict(zip(Roles.nhl, Emojis.nhl))
    NHL_LOGOS_EMOJIS = dict(zip(Roles.nhl_logos, Emojis.nhl_logos))
    # Other
    FCF_EMOJIS = dict(zip(Roles.fcf, Emojis.fcf))
    USFL_EMOJIS = dict(zip(Roles.usfl, Emojis.usfl))
    XFL_EMOJIS = dict(zip(Roles.xfl, Emojis.xfl))
    FOOTBALL_FUSION_EMOJIS = dict(zip(Roles.football_fusion, Emojis.football_fusion))
    # College
    COLLEGE_EMOJIS = dict(zip(Roles.college, Emojis.college))
    COLLEGE_NEON_EMOJIS = dict(zip(Roles.college, Emojis.college_neon))
    COLLEGE_HELMET_EMOJIS = dict(zip(Roles.college, Emojis.college_helmet))
    COLLEGE_LOGOS_EMOJIS = dict(zip(Roles.college_logos, Emojis.college_logos))
    # Media
    SYMBOL_PACK_1_EMOJIS = dict(zip(Roles.symbol_pack_1, Emojis.symbol_pack_1))
    SYMBOL_PACK_1_NEON_EMOJIS = dict(
        zip(Roles.symbol_pack_1_neon, Emojis.symbol_pack_1_neon)
    )
    MEDIA_EMOJIS = dict(zip(Roles.media, Emojis.media))
    DEVTRAITS_EMOJIS = dict(zip(Roles.devtraits, Emojis.devtraits))


emoji_help_menu = {
    "nfl": [
        {"name": "nfl", "desc": f"{EmojisDict.NFL_EMOJIS['New Orleans Saints']} - 32"},
        {
            "name": "nflneon",
            "desc": f"{EmojisDict.NFL_NEON_EMOJIS['New Orleans Saints']} - 32",
        },
        {
            "name": "nflneon2",
            "desc": f"{EmojisDict.NFL_NEON2_EMOJIS['New Orleans Saints']} - 32",
        },
        {
            "name": "nflhelmet",
            "desc": f"{EmojisDict.NFL_HELMET_EMOJIS['New Orleans Saints']} - 32",
        },
        {
            "name": "nfl3d",
            "desc": f"{EmojisDict.NFL_3D_EMOJIS['New Orleans Saints']} - 32",
        },
        {"name": "nfllogos", "desc": f"{EmojisDict.NFL_LOGOS_EMOJIS['NFL']} - 8"},
    ],
    "nba": [
        {
            "name": "nba",
            "desc": f"{EmojisDict.NBA_EMOJIS['Los Angeles Clippers']} - 30",
        },
        {"name": "nbalogos", "desc": f"{EmojisDict.NBA_LOGOS_EMOJIS['NBA']} - 7"},
    ],
    "mlb": [
        {"name": "mlb", "desc": f"{EmojisDict.MLB_EMOJIS['Baltimore Orioles']} - 30"},
        {"name": "mlblogos", "desc": f"{EmojisDict.MLB_LOGOS_EMOJIS['MLB']} - 10"},
    ],
    "nhl": [
        {"name": "nhl", "desc": f"{EmojisDict.NHL_EMOJIS['Seattle Kraken']} - 32"},
        {"name": "nhllogos", "desc": f"{EmojisDict.NHL_LOGOS_EMOJIS['NHL']} - 6"},
    ],
    "college": [
        {
            "name": "college",
            "desc": f"{EmojisDict.COLLEGE_EMOJIS['Clemson Tigers']} - 32",
        },
        {
            "name": "collegehelmet",
            "desc": f"{EmojisDict.COLLEGE_HELMET_EMOJIS['Clemson Tigers']} - 30",
        },
        {
            "name": "collegeneon",
            "desc": f"{EmojisDict.COLLEGE_NEON_EMOJIS['Clemson Tigers']} - 32",
        },
        {
            "name": "collegelogos",
            "desc": f"{EmojisDict.COLLEGE_LOGOS_EMOJIS['NCAA']} - 7",
        },
    ],
    "media": [
        {"name": "media", "desc": f"{EmojisDict.MEDIA_EMOJIS['Fox']} - 14"},
        {
            "name": "devtraits",
            "desc": f"{EmojisDict.DEVTRAITS_EMOJIS['Super Star X Factor']} - 5",
        },
        {
            "name": "symbolpack1",
            "desc": f"{EmojisDict.SYMBOL_PACK_1_EMOJIS['Info']} - 4",
        },
        {
            "name": "symbolpack1neon",
            "desc": f"{EmojisDict.SYMBOL_PACK_1_NEON_EMOJIS['Info']} - 4",
        },
    ],
    "other": [
        {"name": "xfl", "desc": f"{EmojisDict.XFL_EMOJIS['DC Defenders']} - 8"},
        {
            "name": "usfl",
            "desc": f"{EmojisDict.USFL_EMOJIS['New Orleans Breakers']} - 8",
        },
        {"name": "fcf", "desc": f"{EmojisDict.FCF_EMOJIS['Glacier Boyz']} - 8"},
        {
            "name": "footballfusion",
            "desc": f"{EmojisDict.FOOTBALL_FUSION_EMOJIS['Baltimore Royals']} - 32",
        },
    ],
}

role_to_low_error = "My role is to low to give that user that role\nhttps://media.discordapp.net/attachments/817569246103470113/864002780003434545/unknown.png?width=269&height=406"

support_server = BotLinks.support_server

welcome_message = f"<:3DBreadWinnerB:939604485142093844> **Thanks for inviting me to your server** <:3DBreadWinnerB:939604485142093844>\n\n**See my commands with:** `/cmds`\nIf you ever need help, come stop by to my home\n{support_server}"

error_support_message = f"`Having issues or need more help? Try joining the support server:` <{support_server}>"


tips_and_tricks = {
    "fonts": [
      "Keep using the same font over and over? Try using **/font-channel**!",
    ],
    "Symbols": [
      "Try combining multiple symbols together",
      "Look at other peoples' servers for inspiration",
      "Try to make something you have never seen before",
      "Try to make something out of your comfort zone"
    ]
}

  #banner = 
  #"Logos": [
      #{
        #"MainLogo": "",
        #"Christmas": ""
      #}
    #],
    #"Other": [
      #{
        #"PrivacyPolicy": ""
      #}
