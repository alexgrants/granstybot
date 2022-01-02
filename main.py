import discord, time, asyncio, json

from discord.raw_models import RawReactionActionEvent
from discord.ext import commands
intents = discord.Intents.all()


bot = commands.Bot(command_prefix = ".", intents = intents)



# Allumer le bot + status en activité



@bot.event
async def on_ready():
    print("Le bot est prêt !")
    activity = discord.Game(name = "manger des donuts !", type = 4)
    await bot.change_presence(status = discord.Status.online, activity = activity)




# Afficher les erreurs



@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Une erreur est survenue :\n`{error}`")



# ------------------------------------- #
# Afficher membres (arrivées/départs)



global member_channel_id
member_channel_id = 924360382041161758

@bot.event
async def on_member_join(member):
    serveur = member.guild.id
    if serveur == 924360381407838279:
        channel = bot.get_channel(member_channel_id)
        await channel.send(f"**{member.name}** a rejoint `{member.guild.name}`.")
        guild = bot.get_guild(924360381407838279)
        await member.add_roles(guild.get_role(924360381407838282))
    
##########
    
@bot.event
async def on_member_remove(member):
    serveur = member.guild.id
    if serveur == 924360381407838279:
        channel = bot.get_channel(member_channel_id)
        await channel.send(f"**{member.name}** a quitté `{member.guild.name}`.")



# ------------------------------------- #
# Messages pour les idées



@bot.event
async def on_message(message):
    if message.channel.id == 829175293276586024:
        idee = bot.get_channel(829175293276586024)
        if message.author.bot == False:
            await message.delete()
            msg = await idee.send(message.content)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            await idee.send("**------------------------------------**")
    await bot.process_commands(message)

# ------------------------------------- #
# Commande d'affichage pseudo



@bot.command()
async def myname(ctx):
    embed = discord.Embed(color = 0x20EE00)
    embed.add_field(name = "** **", value = f"Votre pseudo discord est **{ctx.author.name}**.")
    await ctx.send(embed = embed)
    


# ------------------------------------- #
# Commande d'affichage pseudo renommé



@bot.command()
async def mynickname(ctx):
    embedbis = discord.Embed(title = False, color = 0x20EE00)
    embedbis.add_field(name = "** **", value = f"Votre pseudo discord est **{ctx.author.display_name}**.")
    await ctx.send(embed = embedbis)



# ------------------------------------- #
# Commande qui donne le grade de la personne



@bot.command()
async def myrank(ctx):
    liste_ranks = ["795094227401834499", "795094227401834497", "839570218736156703", "795094227401834496", "795094227394232337", "811874070420652052", "811873478876594186", "811873259124555787", "812664627824951329", "798091823913369600", "798091604354531358", "795094227394232334"]
    for role in ctx.author.roles:
        if str(role.id) in liste_ranks:
            await ctx.send(f"Vous occupez le grade suivant : **{role.name}**.")
            return
    await ctx.send("Vous n'avez aucun grade.")



# ------------------------------------- #
# Commande infos serveur
    


@bot.command()
async def infos_server(ctx):
    server = ctx.guild
    nb_personnes = server.member_count
    nb_textuels = len(server.text_channels)
    nb_vocaux = len(server.voice_channels)
    nom_server = server.name
    embed = discord.Embed(title = nom_server, description = "Voici quelques données sur ce serveur.", color = 0x20EE00)
    embed.set_thumbnail(url = "https://e7.pngegg.com/pngimages/477/329/png-clipart-gear-encapsulated-postscript-computer-icons-gears-miscellaneous-transport.png")
    embed.add_field(name = ":family:", value = f"**- Le serveur contient** `{nb_personnes}` **personnes.**", inline = False)
    embed.add_field(name = ":loudspeaker:", value = f"**- Le serveur contient** `{nb_vocaux}` **salons vocaux.**", inline = False)
    embed.add_field(name = ":pencil:", value = f"**- Le serveur contient** `{nb_textuels}` **salons textuels.**", inline = False)
    await ctx.send(embed = embed)



# ------------------------------------- #
# Commande de clear



@bot.command()
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    nbr = 0
    for message in messages:
        nbr += 1
        await message.delete()
    if nbr == 1:    
        await ctx.send(f"`{nbr}` message a été supprimé avec succès ! :wastebasket:", delete_after = 15)
    else:
        await ctx.send(f"`{nbr}` messages ont été supprimés avec succès ! :wastebasket:", delete_after = 15)



# ------------------------------------- #
# Commande de création d'un salon



@bot.command()
async def ctc(ctx, name):
    await ctx.guild.create_text_channel(name)
      


# ------------------------------------- #
# Aller manger !
    


@bot.command()
async def eat(ctx):
    embed = discord.Embed(title = "**Je vais manger, à tout de suite !**", color = 0x20EE00)
    embed.set_thumbnail(url = "https://o1.llb.be/image/thumb/5617d5763570b0f19f3eaf66.jpg")
    await ctx.send(embed = embed)



# ------------------------------------- #
# Commande absence



@bot.command()
async def abs(ctx, date1, date2, *raison):
    raison1 = ""
    for word in raison:
        raison1 += " " + word
    await ctx.send(f"- __**{ctx.author.display_name}**__ sera absent du `{date1}` au `{date2}` pour la raison suivante : ***{raison1}***.")



# ------------------------------------- #
# Commande PDS



liste_service = []

@bot.command()
async def pds(ctx):
    if ctx.author.display_name in liste_service:
        await ctx.send("Vous êtes déjà en service !")
    else:
        liste_service.append(ctx.author.display_name)
        char_liste = ""
        embed = discord.Embed(title = "Agents en service :", color = 0x532090)
        for agent in liste_service:
            char_liste +=  "\n - " + agent
        char_liste += "\n"
        embed.add_field(name = "** **", value = char_liste)
        await ctx.send(embed = embed)

#############

@bot.command()
async def fds(ctx):
    if ctx.author.display_name in liste_service:
        liste_service.remove(ctx.author.display_name)
        await ctx.send("Vous n'êtes désormais plus en service.")
        if len(liste_service) == 0:
            await ctx.send("**Plus personne n'est en service !**")
        else:
            char_liste = ""
            embed = discord.Embed(title = "Agents en service :", color = 0x532090)
            for agent in liste_service:
                char_liste += "\n - " + agent
            char_liste += "\n"
            embed.add_field(name = "** **", value = char_liste)
            await ctx.send(embed = embed)
    else:
        await ctx.send("Vous n'êtes pas en service.")



# ------------------------------------- #
# Message channel ressource + edit message



@bot.command()
async def chan(ctx):
    embed = discord.Embed(title = "**Canal UHF utilisé :**", description = "Ce canal est à configurer sur la radio lorsque vous êtes en service.", color = 0x3885E7)
    embed.add_field(name = "Canal", value = "`001`")
    embed.set_footer(text = "Attention, ce canal ne peut en aucun cas être éloqué en la présence de civils et ne peut être écouté hors temps de service.", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")
    global msg_chan
    msg_chan = await ctx.send(embed = embed)

#############

channel_id = 860943917474512916
message_id = 921074062296485979

@bot.command()
async def edit_chan(ctx, arg1):
    embed = discord.Embed(title = "**Canal UHF utilisé :**", description = "Ce canal est a configurer sur la radio lorsque vous êtes en service.", color = 0x3885E7)
    embed.add_field(name = "Canal", value = f"`{arg1}`")
    embed.set_footer(text = "Attention, ce canal ne peut en aucun cas être éloqué en la présence de civils et ne peut être écouté hors temps de service.", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")
    msg = await bot.get_channel(channel_id).fetch_message(message_id)
    msg2 = bot.get_channel(channel_id)
    await msg.edit(embed = embed)
    await msg2.send("<@&863333137152213002>, changement de canal !", delete_after = 3600)
    await ctx.send(f"L'édition du canal s'est effectuée avec succès. Le nouveau canal est le **{arg1}**.", delete_after = 30)
    


# ------------------------------------- #
# Réaction message bot



@bot.command()
async def reaction_msg(ctx):
    global msg
    msg = await ctx.send("La boisson est froide !")
    global channel_id
    channel_id = msg.channel.id
    emoji = "🥂"
    await msg.add_reaction(emoji)

##########

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == channel_id:
        if payload.member.bot == False:
            member = payload.member
            await msg.remove_reaction("🥂", member)
            msgt = bot.get_channel(channel_id)
            await msgt.send("Je te vois. 👀")



# ------------------------------------- #
# Commande avertissement orthographe



@bot.command()
async def ortho(ctx, identifiant : int, user_id):
    salon = bot.get_channel(identifiant)
    user_id = "<@" + user_id + ">"
    await salon.send(f"Attention aux fautes d'orthographes. {user_id}", delete_after = 3600)



# ------------------------------------- #
# Commandes pour le shift

liste_shift_l = [] 
liste_shift_a = []          # Stocke les noms des agents
liste_shift_w = []

agents_l = []
agents_a = []               # Stocke la liste des agents avec les tirets          
agents_w = []

id_unit_l = []
id_unit_a = []              # Stocke l'id des unitées
id_unit_w = []

number_1 = 0                

@bot.command()
async def start_shift(ctx):
    global number_1
    role = bot.get_guild(464524458976083978).get_role(522142563570810925)
    if role in ctx.author.roles:
        if number_1 == 0:
            await ctx.send("Vous venez lancer un shift.")
            number_1 += 1
            return number_1
        else:
            await ctx.send("Un shift est déjà en cours !")
    else:
        await ctx.send("Vous n'êtes pas superviseur, par conséquent, vous ne pouvez exécuter cette commande.")

@bot.command()
async def stop_shift(ctx):
    global number_1
    if number_1 > 0:
        role = bot.get_guild(795094227360546816).get_role(812698869140815885)
        if role in ctx.author.roles:
            await ctx.send("Vous venez de mettre fin au shift.")
            number_1 -= 1
            return number_1
        else:
            await ctx.send("Vous n'êtes pas superviseur, par conséquent, vous ne pouvez exécuter cette commande.")
    else:
        await ctx.send("Aucun shift n'est en cours.")

@bot.command()
async def create_unit(ctx, type_unit, id_unit : int):
    if number_1 > 0:
        if type_unit == "l" or type_unit == "lincoln":
            if ctx.author.display_name in liste_shift_l or ctx.author.display_name in liste_shift_a or ctx.author.display_name in liste_shift_w:
                await ctx.send("Vous êtes déjà sur la fiche de patrouille.")
            elif id_unit in id_unit_l:
                await ctx.send(f"L'identifiant {id_unit} est déjà utilisé.")
            else:
                if 0 < id_unit < 10:
                    await ctx.send(f"Vous venez de déclarer une unité de type `lincoln` avec comme identifiant de patrouille **0{id_unit}**.")
                else:
                    await ctx.send(f"Vous venez de déclarer une unité de type `lincoln` avec comme identifiant de patrouille **{id_unit}**.")
                global agents_l
                agents_l = ""
                liste_shift_l.append(ctx.author.display_name + " " + id_unit)
                for agent_l in liste_shift_l:
                    if 0 < id_unit < 10:
                        agents_l += "\n - " + agent_l + " " + "|" + " " + "1" + "L" + "0" + str(id_unit)
                    else:
                        agents_l += "\n - " + agent_l + " " + "|" + " " + "1" + "L" + str(id_unit)
                    return agents_l
        else:
            if type_unit != "l" or type_unit != "lincoln":
                await ctx.send("Le type de l'unité entré est incorrect, refaites la commande !")
            elif type_unit == "":
                await ctx.send("Vous n'avez pas précisé le type de l'unité, refaites la commande !")
            else:
                await ctx.send("Le l'identifiant de patrouille entré est incorrect. Il doit être compris entre 01 et 99.")
        if type_unit == "a" or type_unit == "adam":
            if ctx.author.display_name in liste_shift_l or ctx.author.display_name in liste_shift_a or ctx.author.display_name in liste_shift_w:
                await ctx.send("Vous êtes déjà sur la fiche de patrouille.")
            else:
                if 0 < id_unit < 10:
                    await ctx.send(f"Vous venez de déclarer une unité de type `adam` avec comme identifiant de patrouille **0{id_unit}**.")
                else:
                    await ctx.send(f"Vous venez de déclarer une unité de type `adam` avec comme identifiant de patrouille **{id_unit}**.")
                global agents_a
                agents_a = ""
                liste_shift_a.append(ctx.author.display_name)
                for agent_a in liste_shift_a:
                    if 0 < id_unit < 10:
                        agents_a += "\n - " + agent_a + " " + "|" + " " + "1" + "A" + "0" + str(id_unit)
                    else:
                        agents_a += "\n - " + agent_a + " " + "|" + " " + "1" + "A" + str(id_unit)
                    return agents_a
        else:
            if type_unit != "a" or type_unit != "adam":
                await ctx.send("Le type de l'unité entré est incorrect, refaites la commande !")
            elif type_unit == "":
                await ctx.send("Vous n'avez pas précisé le type de l'unité, refaites la commande !")
            else:
                await ctx.send("Le l'identifiant de patrouille entré est incorrect. Il doit être compris entre 01 et 99.")
        if type_unit == "w" or type_unit == "william":
            if ctx.author.display_name in liste_shift_l or ctx.author.display_name in liste_shift_a or ctx.author.display_name in liste_shift_w:
                await ctx.send("Vous êtes déjà sur la fiche de patrouille.")
            else:
                if 0 < id_unit < 10:
                    await ctx.send(f"Vous venez de déclarer une unité de type `william` avec comme identifiant de patrouille **0{id_unit}**.")
                else:
                    await ctx.send(f"Vous venez de déclarer une unité de type `william` avec comme identifiant de patrouille **{id_unit}**.")
                global agents_w
                agents_w = ""
                liste_shift_w.append(ctx.author.display_name)
                for agent_w in liste_shift_w:
                    if 0 < id_unit < 10:
                        agents_w += "\n - " + agent_w + " " + "|" + " " + "1" + "W" + "0" + str(id_unit)
                    else:
                        agents_w += "\n - " + agent_w + " " + "|" + " " + "1" + "W" + str(id_unit)
                    return agents_w
        else:
            if type_unit != "w" or type_unit != "william":
                await ctx.send("Le type de l'unité entré est incorrect, refaites la commande !")
            elif type_unit == "":
                await ctx.send("Vous n'avez pas précisé le type de l'unité, refaites la commande !")
            else:
                await ctx.send("Le l'identifiant de patrouille entré est incorrect. Il doit être compris entre 01 et 99.")
    else:
        await ctx.send("Aucun shift n'est en cours !")
    

@bot.command()
async def i_shift(ctx):
    if number_1 == 0:
        await ctx.send("Aucun shift n'est en cours.")
    else:
        embed_shift = discord.Embed(title = "Fiche de shift en cours :", color = 0xCF7C1E)
        if len(agents_l) == 0:
            embed_shift.add_field(name = "Unité(s) `lincoln` occupée(s) :", value = "Aucune unité n'occupe le type d'unités `lincoln`.", inline = False)
        else:
            embed_shift.add_field(name = "Unité(s) `lincoln` occupée(s) :", value = agents_l, inline = False)
        if len(agents_a) == 0:
            embed_shift.add_field(name = "Unité(s) `adam` occupée(s) :", value = "Aucune unité n'occupe le type d'unités `adam`.", inline = False)
        else:
            embed_shift.add_field(name = "Unité(s) `adam` occupée(s) :", value = agents_a, inline = False)
        if len(agents_w) == 0:
            embed_shift.add_field(name = "Unité(s) `william` occupée(s) :", value = "Aucune unité n'occupe le type d'unités `william`.")
        else:
            embed_shift.add_field(name = "Unité(s) `william` occupée(s) :", value = agents_w)
        await ctx.send(embed = embed_shift)



# ------------------------------------- #
# Commandes pour les documents de police.



@bot.command()
async def doc(ctx):
    if ctx.author.id == 371009536158597121:
        embed = discord.Embed(title = "**Code d'éthique de l'application de la loi**", color = 0xCF1E69)
        embed.add_field(name = "** **", value = """*"En tant qu'agent chargé de l'application de la loi, mon devoir fondamental est de servir l'humanité: protéger les vies et les biens, protéger les innocents contre la duperie, les faibles contre l'oppression ou l'intimidation, et le pacifique contre la violence ou le désordre, et de respecter les droits constitutionnels de tous les hommes à la liberté, à l'égalité et à la justice.*""", inline = False)
        embed.add_field(name = "** **", value = """*Je garderai ma vie privée comme un exemple pour tous; garder son calme courageux face au danger, au mépris ou au ridicule; développer la maîtrise de soi; et être constamment attentif au bien-être des autres. Honnête dans mes pensées et dans mes actes tant dans ma vie personnelle que dans ma vie officielle, je respecterai de manière exemplaire les lois du pays et les règlements de mon département. Tout ce que je vois ou entends qui a un caractère confidentiel ou qui m’est confié à titre officiel restera toujours secret à moins que la révélation ne soit nécessaire dans l’exercice de mes fonctions.*""", inline = False)
        embed.add_field(name = "** **", value = """*Je n'agirai jamais de manière officieuse et ne laisserai jamais des sentiments personnels, des préjugés, des animosités ou des amitiés influencer mes décisions. Sans compromis pour le crime et avec des poursuites sans relâche pour les criminels, je ferai respecter la loi avec courtoisie et de manière appropriée, sans crainte ni favoritisme, sans malveillance ni mauvaise volonté, sans jamais avoir recours à la force ou à la violence et ne jamais accepter de gratification.*""", inline = False)
        embed.add_field(name = "** **", value = """*Je reconnais le badge de mon bureau comme un symbole de la confiance du public et je l'accepte comme une confiance du public à conserver tant que je suis fidèle à l'éthique du service de police. Je m'efforcerai constamment d'atteindre ces objectifs et idéaux, en me consacrant à la profession que je me suis donnée: faire respecter la loi."*""")
        await ctx.send(embed = embed)
    else:
        await ctx.send("Vous n'avez pas accès à cette commandedatetime A combination of a date and a time. Attributes: ()")

@bot.command()
async def doc_2(ctx):
    embed = discord.Embed(title = "**Vocabulaire fréquenciel**", color = 0xCF1E69)
    embed.add_field(name = "__Codes radio les plus utiles/utilisés :__", value = """
    ㅤ
    - `CODE 1 :` Prise de l'appel
    - `CODE 2 :` Appel de routine, circulation sans avertisseurs lumineux/sonores
    - `CODE 2+ :` Appel prioritaire, circulation avec lumières seulement
    - `CODE 3 :` Appel d'urgence, circulation avec avertisseurs lumineux/sonores
    - `CODE 4 :` Situation sous contrôle/terminée, aucune unité supplémentaire requise
    - `CODE 5 :` Restez à distance du lieu d'intervention
    - `CODE 6 :` Recherche/Investigation dans la zone autour de l'appel
    - `CODE 7 :` Pause déjeuner
    - `CODE 9 :` Blockage de la circulation
    - `CODE 10 :` Silence radio, information importante à donner
    - `CODE 20 :` Appeler les médias
    - `CODE 37 :` Véhicule volé signalé
    - `CODE 77 :` Attention, possible embuscade
    - `CODE 99 :` Urgence absolue
    ㅤ
    """, inline = False)
    embed.add_field(name = "__Codes radio pour le(s) type(s) d'appel(s) :__", value = """
    ㅤ
    - `148 :` Refus d'obtempérer
    - `187 :` Homicide
    - `207 :` Kidnapping
    - `211 :` Braquage avec suspects armés
    - `211 Silencieux :` Braquage avec déclenchement d'alarme silencieuse
    - `240 :` Attaque de tout type
    - `246 :` Attaque avec une arme léthale
    - `417 :` Personne avec une arme
    - `459 :` Cambriolage
    - `480 :` Délit de fuite
    - `487 :` Vol de voiture
    - `502 :` Conduite sous influence
    ㅤ
    """, inline = False)
    embed.add_field(name = "__Alphabet phonétique :__ *(Utilisé par exemple lors d'une description de plaque)*", value = """
    ㅤ
    ```
    A  Adam                              N  Nora
    B  Boy                               O  Ocean
    C  Charles                           P  Paul
    D  David                             Q  Queen
    E  Edward                            R  Robert
    F  Frank                             S  Sam
    G  George                            T  Tom
    H  Henry                             U  Union
    I  Ida                               V  Victor
    J  John                              W  William
    K  King                              X  X-Ray
    L  Lincoln                           Y  Yellow
    M  Mary                              Z  Zebra```
    """)
    await ctx.send(embed = embed)

@bot.command()
async def doc_3(ctx):
    embed = discord.Embed(title = "**Identifiants de patrouille**", color = 0xCF1E69)
    embed.add_field(name = "__Identifiants fréquenciels :__", value = """
    ㅤ
    `A / ADAM :` Deux Officiers dans un véhicule de patrouille
    `SLO :` Trois Officiers dans un véhicule de patrouille
    `C / CHARLES :` Parking enforcement
    `E / EDWARD :` Traffic enforcement
    `L / LINCOLN :` Un seul Officier dans un véhicule de patrouille
    `M / MARY :` Patrouille en motos (à 2)
    `N / NORA :` Unité unmarked
    `V / Victor :` Unité en vélo
    `W / WILLIAM :` Unité détective
    ㅤ""", inline = False)
    embed.add_field(name = "__Modèle d'identifiant radio :__", value = """
    ㅤ
    **01** (Division Mission Row) **- Type d'unité** *(voir au-dessus)* **- Numéro d'unité**
    ㅤ
    Le numéro d'unité est assigné à chaque patrouilleur par le superviseur.
    ㅤ
    __**EXEMPLE :**__ **01 - Lincoln - 01 | 01 - ADAM - 01**
    ㅤ
    __ADAM :__
    - Le passager fait systématiquement les communications radio.
    ㅤ
    __HENRY :__
    - Le nom *"Henry"* est pour le type d'unité, et pas un identifiant radio. L'ID radio de l'ASD est **AIR** (Sans le numéro de division devant).
    ㅤ
    _Exemples d'identifiant radio pour une unité_ ***HENRY :*** **AIR-01 / AIR-02 /** etc.

    _PS :_ Vous pouvez utiliser les abréviations suivantes en radio : **1A01 / 1L01**""")
    await ctx.send(embed = embed)

@bot.command()
async def doc_4(ctx):
    embed = discord.Embed(title = "**Présentation vestimentaire**", color = 0xCF1E69)
    embed.add_field(name = "**Manches longues avec cravate :**", value = """
    ㅤ
    ```
     HOMMES
    T-Shirt 1 : 58
    T-Shirt 2 : 0
    Torse 1 : 287
    Torse 2 : 0
    Calques : 31 ( cf. #rangs-du-lspd / Officier III et +)
    Bras : 4
    Chaîne : 8
    Jambes 1 : 69
    Jambes 2 : 0
    Masque : 156
    Chaussures : 19
    Sac : 57
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ
    ```
     FEMMES
    T-Shirt : 105
    T-Shirt 2 : 0
    Torse 1 : 311
    Torse 2 : 0
    Bras : 14
    Chaîne : 8
    Jambes 1 : 70
    Jambes 2 : 0
    Chaussures : 25
    Sac : 52 
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ""", inline = False)
    embed.add_field(name = "**Manches courtes :**", value = """
    ㅤ
    ```
    T-Shirt 1 : 58
    T-Shirt 2 : 0
    Torse 1 : 277
    Torse 2 : 0 (1 -> Traffic Division)
    Calques : 31 ( cf. #rangs-du-lspd / Officier III et +)
    Bras : 11
    Chaîne : 8
    Jambes 1 : 69
    Jambes 2 : 0
    Masque : 156
    Chaussures : 19
    Sac : 57
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ
    ***Les*** <@&795094227394232334> ***seront*** __***toujours***__ ***en manches longues et avec la cravate.***
    ㅤ""", inline = False)
    embed.add_field(name = "**Manches longues** __**sans**__ **cravate :**", value = """
    ㅤ
    ```
    T-Shirt 1 : 58
    T-Shirt 2 : 0
    Torse 1 : 280
    Torse 2 : 0
    Calques : 31 ( cf. #rangs-du-lspd / Officier III et +)
    Bras : 4
    Chaîne : 8
    Jambes 1 : 69
    Jambes 2 : 0
    Masque : 156
    Chaussures : 19
    Sac : 57
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ""", inline = False)
    embed.add_field(name = "**Anti-émeutes :**", value = """
    ㅤ
    ```
    T-Shirt 1 : 97
    T-Shirt 2 : 0
    Torse 1 : 277
    Torse 2 : 0
    Calques : 31 ( cf. #rangs-du-lspd / Officier III et +)
    Bras : 11
    Chaîne : 8
    Casque : 63
    Jambes 1 : 69
    Jambes 2 : 0
    Masque : 156
    Chaussures : 19
    Sac : 57
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ""", inline = False)
    embed.add_field(name = "**Cérémonie :**", value = """
    ㅤ
    ```
    T-Shirt 1 : 58
    T-Shirt 2 : 0
    Torse 1 : 287
    Torse 2 : 0
    Calques : 28 ( cf. #rangs-du-lspd / Officier III et +)
    Bras : 81
    Chaîne : 8
    Jambes 1 : 69
    Jambes 2 : 0
    Casque : 50
    Chaussures : 19
    Sac : 57
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ
    __À faire au magasin de vêtement BLOC 215 :__""", inline = False)
    embed.add_field(name = "**Uniforme avec veste légère :**", value = """
    ㅤ
    ```
    T-Shirt 1 : 67 / 68 (Avec cravate pour les Officiers I)
    T-Shirt 2 : 0
    Torse 1 : 116
    Torse 2 : 0 (1 -> Traffic Division)
    Calques : 0 
    Gilet par-balles : 72
    Bras : 4
    Chaîne : 8
    Jambes 1 : 69
    Jambes 2 : 0
    Masque : 156
    Chaussures : 19
    Sac : 57
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ""", inline = False)
    embed.add_field(name = "**Uniforme avec veste de pluie :**", value = """
    ㅤ
    ```
    T-Shirt 1 : 67 / 68 (Avec cravate pour les Officiers I)
    T-Shirt 2 : 0
    Torse 1 : 274
    Torse 2 : 0 (1 -> Traffic Division)
    Calques : 0
    Gilet par-balles : 72
    Bras : 4
    Chaîne : 8
    Jambes 1 : 69
    Jambes 2 : 0
    Masque : 156
    Chaussures : 19
    Sac : 57
    Couleur sac : 0 (Officier III) / 1 (Sergeants) / etc.```
    ㅤ""")
    embed.set_footer(text = "Le non-respect du port de l'uniforme en service peut conduire à de lourdes sanctions.", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")
    await ctx.send(embed = embed)

@bot.command()
async def doc_5(ctx):
    embed = discord.Embed(title = "**Organigramme du département**", color = 0x0F5D9E)
    embed2 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed2.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959222025682954/CPT.png")
    embed2.add_field(name = "Captain", value = """
    ㅤ
    *Un Captain, ressemblant à un directeur de district au sein d'une grande société, sert en tant que commandant d'une division. Il est chargé d'inspecter et de superviser les fonctions des patrouilleurs et des Detectives pour assurer la conformité aux politiques, procédures, règlements et normes ; de superviser les fonctions administratives et de soutien du personnel ; d'inspecter le personnel, les installations et les tactiques pour les besoins en matière de sécurité et/ou de formation ; de maintenir l'entretient avec le gouvernement, les organisations civiques et les citoyens et d'entretenir des relations pour faciliter les fonctions du Département et promouvoir la sécurité des programmes de police.*
    ㅤ
    """)
    embed3 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed3.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959212382060615/LTN.png")
    embed3.add_field(name = "Lieutenant I/II", value = """
    ㅤ
    *Un Lieutenant peut aider les Détectives des divisions commandantes ou agir en tant qu'officier de section responsable de diverses entités spécialisées dans l'ensemble du LSPD. Selon la division de l'affectation, un Lieutenant peut superviser les activités de ses subordonnés ; coordonner l'entraînement et assurer un stock suffisant de fournitures et d'équipement tactiques ; maintenir des entretiens avec les entités appropriées du département ; agir en tant que chef sur un lieux de crime ; et/ou examiner et remplir tous les rapport pour approbation d'un Captain.*
    ㅤ
    """)
    embed4 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed4.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959202307211294/SGT_II-removebg-preview.png")
    embed4.add_field(name = "Sergeant II", value = """
    ㅤ
    *Un Sergeant II, le chef de poste, est un poste de supervision avec des affectations spécialisées et administratives. Un Sergeant II supervise un groupe d'agents de police, les Sergeants I, et les instruit dans l'exercice des fonctions qui leur sont assignées.*
    ㅤ
    """)
    embed5 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed5.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959192739872828/SGT_I-removebg-preview.png")
    embed5.add_field(name = "Sergeant I", value = """
    ㅤ
    *Un Sergeant I est un chef de service, tout comme un Sergeant II. Il supervise une escouade ou un groupe spécifique d'agents de police. Un Sergeant I est tenu de donner des instructions au personnel affecté dans l'exercice de ses fonctions requises. La capacité de base d'un Sergeant I est la supervision sur le terrain et des opérations, mais des affectations administratives et spécialisées sont également disponibles. Certains Sergeants effectuent des enquêtes initiales et de suivi sur les crimes à la demande d'un Détective.*
    ㅤ
    """)
    embed6 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed6.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959181483409418/DET_III-removebg-preview.png")
    embed6.add_field(name = "Detective III", value = """
    ㅤ
    *Un Detective III est le responsable de la Detective Division au sein d'une division du LSPD. Il est chargé de servir de chef de file dans des cas très médiatisés de vol, braquages, assasinats, homicides, prises d'otages et attentats terroristes, en plus des fonctions d'un Détective I et II. Un Detective III examine les rapports préparés par ses subordonnés, informe le commandant de l'état d'avancement des enquêtes en cours, fournit une expertise, forme et supervise les Détectives et le personnel civil nouvellement affectés.*
    ㅤ
    """)
    embed7 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed7.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959164621389824/DET_II-removebg-preview.png")
    embed7.add_field(name = "Detective II", value = """
    ㅤ
    *Le poste de Detective II est un poste de supervision. Il est responsable de la formation et de la supervision des activités des Detective I. Certaines des fonctions spécialisées exercées par un Detective II comprennent : mener des enquêtes sur un trafic de drogue, effectuer une surveillance, établir et maintenir des contacts avec des informateurs ; enquêter sur les crimes liés aux gangs ; répondre et enquêter sur les scènes de crimes tels que les homicides, braquages, vols, prises d'otages et attentats terroristes. En outre, un Detective II peut exercer des fonctions de liaison judiciaire, fournir des témoignages d'experts devant les tribunaux et mener des enquêtes sur les crimes commis par des gangs d'origine étrangère.*
    ㅤ
    """)
    embed8 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed8.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959137815592990/PO_III1-removebg-preview.png")
    embed8.add_field(name = "Officer III+1", value = """
    ㅤ
    *Un Officier III+1 (PO III + 1), familièrement appelé «officier», est la désignation est donnée à certains officiers de police III dans des situations spéciales.
    ㅤ
    Ceux-ci incluent, mais sans s'y limiter, les enquêteurs de la circulation, les gestionnaires K9, les chefs d'escouade assistants SWAT et les officiers principaux supérieurs qui coordonnent les zones géographiques.*
    ㅤ
    """)
    embed9 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed9.set_thumbnail(url = "https://media.discordapp.net/attachments/541559588659658774/856959125980053514/PO_III-removebg-preview.png")
    embed9.add_field(name = "Officer III", value = """
    ㅤ
    *Un Officier III est chargé d'appliquer les lois et les ordres, de protéger la vie et les biens, de délivrer des citations, de procéder à des arrestations, de préparer des rapports, de rencontrer les membres de la communauté, de travailler en équipe et de fournir des informations au public et aux unités départementales. Ce poste peut également superviser en tant qu'officier formateur d'un officier I sur le terrain (FTO).*
    ㅤ
    """)
    embed10 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed10.add_field(name = "Officer II", value = """
    ㅤ
    *Un Officier II est affecté à une division de patrouille de la ville de Los Santos où il doit utiliser toutes les connaissances et tactiques apprises à l'académie. À l'étape suivante de l'échelle promotionnelle, un Officier II est toujours considéré comme un agent probatoire et est placé sous la supervision d'un grade supérieur, généralement un Officier III, officier de formation sur le terrain (FTO).*
    ㅤ
    """)
    embed11 = discord.Embed(title = "** **", color = 0x0F5D9E)
    embed11.add_field(name = "Officer I (aussi surnommé par « un bleu / rookie »)", value = """
    ㅤ
    *C'est la première étape de l'échelle de carrière au sein du LSPD. Il s'agit de la classification d'entrée de gamme donnée à tous les agents du LSPD à l'entrée dans une division. Ils sont formés en continu à la tactique, aux armes à feu et à la conduite. Un Officier I passe automatiquement au grade d'Officier II après avoir terminé avec succès sa période probatoire de 2 semaines, et après validation de son FTO ou d'un Sergeant.*
    ㅤ
    """)

    await ctx.send(embed = embed)
    time.sleep(2)
    await ctx.send(embed = embed2)
    time.sleep(2)
    await ctx.send(embed = embed3)
    time.sleep(2)
    await ctx.send(embed = embed4)
    time.sleep(2)
    await ctx.send(embed = embed5)
    time.sleep(2)
    await ctx.send(embed = embed6)
    time.sleep(2)
    await ctx.send(embed = embed7)
    time.sleep(2)
    await ctx.send(embed = embed8)
    time.sleep(2)
    await ctx.send(embed = embed9)
    time.sleep(2)
    await ctx.send(embed = embed10)
    time.sleep(2)
    await ctx.send(embed = embed11)

@bot.command()
async def doc_6(ctx):
    embed = discord.Embed(title = "**Les Droits Miranda**", color = 0x1ABA80)
    embed.add_field(name = "__Partie 1 :__", value = """
    ㅤ
    Mr/Mme **[Nom et Prénom]**
    Nous somme actuellement le **[Date]**, il est présentement **[Heure]**. 
    Vous êtes arrêté pour les chefs d'accusation suivants : **[Citez le/les délits]**.
    ㅤ
    Vous avez le droit de garder le silence. Si vous renoncez à ce droit, tout ce que vous direz pourra être et sera utilisé contre vous devant une cour de justice.
    Vous avez le droit à un avocat et d'avoir un avocat présent lors de votre interrogatoire. 
    Si vous n'en avez les moyens, un vous sera commis d'office. 
    Une fois en cellule vous aurez le droit à des soins médicaux ainsi que des vivres alimentaires.
    Vous avez le droit d'exercer ces droits à tout moment.
    ㅤ""", inline = False)
    embed.add_field(name = "__Partie 2 :__", value = """
    ㅤ
    Avez vous compris vos droits Mr/Mme **[Nom]** ?
    ㅤ
    *PS : Si l'individu répond par la négation, vous pouvez le lui répéter jusqu’à `3` fois en recommencant au début. Au delà de ces 3 répétitions, vous pouvez considérer que l'individu a bien compris ses droits.*
    ㅤ
    On peut aussi ajouter,
    En ayant ces droits à l'esprit, avez vous l'envie de vous exprimer ?
    """)
    embed.set_footer(text = "⚠️ Dans le cas où ces droits ne sont pas cités lors de l'arestation d'un individu, ce dernier peut se voir relaché par l'intervention de son avocat pour n'avoir pas eu connaissance de ces droits.", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")
    await ctx.send(embed = embed)

@bot.command()
async def doc_7(ctx):
    embed = discord.Embed(title = "**Contrôles routiers**", color = 0xE5660E)
    embed.add_field(name = "__Phase 1 :__", value = """
    ㅤ
    **1 -** Signalisation du contrôle en radio **(ex: 1-A-01 j'annonce un 10-38 sur un véhicule [TYPE] sur [NOM DE LA ROUTE] [DIRECTION])**.
    ㅤ
    **2 -** Allumer ses gyrophares __UNIQUEMENT__ et faire des appels de sirènes. 
    ㅤ
    **3 -** Une fois le véhicule arrêté, laisser :
    ㅤ
    ㅤㅤㅤ-> 1 distance d'environ un véhicule entre le véhicule de 
    ㅤㅤㅤㅤpatrouille et le véhicule contrôlé si le suspect.
    ㅤㅤㅤ-> 1 distance d'environ un véhicule et demi entre le véhicule 
    ㅤㅤㅤㅤde patrouille et le véhicule contrôlé si le suspect est 
    ㅤㅤㅤㅤconsidéré comme étant potentiellement dangereux.
    ㅤㅤㅤ-> 1 distance de 2 véhicules entre le véhicule de patrouille et 
    ㅤㅤㅤㅤle véhicule contrôlé si le suspect est signalé comme étant 
    ㅤㅤㅤㅤdangereux.
    ㅤㅤㅤ-> Braquer les roues du véhicule de patrouille vers la route, et 
    ㅤㅤㅤㅤgarer le véhicule de patrouille de sorte à ce que le feu droit 
    ㅤㅤㅤㅤéclaire la plaque du véhicule contrôlé.
    ㅤ
    `IMAGE 1`""")
    embed.set_image(url = "https://cdn.discordapp.com/attachments/541559588659658774/856990764641943572/unknown.png")
    
    embed2 = discord.Embed(title = "** **", color = 0xE5660E)
    embed2.add_field(name = "__Phase 2 :__", value = """
    ㅤ
    **4 -** Le conducteur et ses passager doivent rester dans leur véhicule tout au long du contrôle. Veillez à vous placer au niveau de la portière arrière du véhicule contrôlé afin d'avoir une visibilité sur ses pieds si elle cache une arme et pour qu'elle ait du mal à se tourner vers vous si elle cherche à vous tirer dessus (cf. Image 2). Si le véhicule est occupé à l'arrière également, dans ce cas là, l'officier devra demander du back-up et devra, une fois celui-ci sur place, faire quitter les occupants du véhicule.
    ㅤㅤㅤ
    **5 -** Entamer la conversation :
    ㅤ 
    ㅤㅤㅤ-> "Bonjour, [GRADE] [NOM] du LSPD, veuillez couper le 
    ㅤㅤㅤㅤcontact et me présenter [PERMIS DE CONDUIRE] et 
    ㅤㅤㅤㅤ[PAPIERS DU VEHICULE]."
    ㅤㅤㅤ-> Faire les vérifications auprès du DISPATCH/MDT 
    ㅤㅤㅤㅤ(Intranet) de l'identité et/ou de la plaque.
    ㅤ""", inline = False)
    embed2.add_field(name = "Deux cas possibles :", value = """
    ㅤㅤㅤㅤ
    ㅤㅤㅤSi le véhicule/la personne ne présente aucun signalement :
    ㅤㅤㅤ-> Retourner auprès du véhicule contrôlé, lui annoncer le 
    ㅤㅤㅤㅤmotif du contrôle, faire le nécessaire niveau amendes 
    ㅤㅤㅤㅤsi besoin, puis lui rendre les papiers.
    ㅤㅤㅤ-> Terminer la conversation poliment, puis signaler à la 
    ㅤㅤㅤㅤpersonne qu'elle peut partir une fois que vous êtes entré 
    ㅤㅤㅤㅤdans votre véhicule.
    ㅤㅤㅤ
    ㅤㅤㅤSi la personne est signalée :
    ㅤㅤㅤ-> Lui demander de sortir du véhicule et de mettre les mains 
    ㅤㅤㅤㅤderrière la tête tout en lui signalant la raison de son 
    ㅤㅤㅤㅤarrestation. 
    ㅤㅤㅤㅤAppelez des unités supplémentaire si nécessaire 
    ㅤㅤㅤㅤ(conseillé).
    ㅤㅤㅤ-> Procéder à l'arrestation.
    ㅤ
    `IMAGE 2`""")
    embed2.set_image(url = "https://media.discordapp.net/attachments/541559588659658774/856996865466695700/unknown.png")
    
    await ctx.send(embed = embed)
    await ctx.send(embed = embed2)

@bot.command()
async def doc_8(ctx):
    embed = discord.Embed(title = "**1. Les poursuites**", color = 0x14C89A)
    embed.add_field(name = "** **", value = """- Lorsqu'une unité part à la poursuite d'un véhicule, elle doit informer les autres unités et/ou le superviseur qu'elle est "en poursuite" et donner l'identification de l'unité, son emplacement et sa direction, une description du véhicule poursuivi et/ou des suspects, les instructions prises et la raison de la poursuite. Une unité aérienne de secours et un superviseur en uniforme disponible peuvent se rendre sur la poursuite en le signalant en radio. L'unité 1ère sur poursuite présente des rapports d'étape fréquents et complets.""", inline = False)
    embed.add_field(name = "** **", value = """- Lorsqu'une unité se joint à une poursuite, elle doit impérativement le signaler en radio par "[id radio] ...ème sur poursuite". Elle ne doit en aucun cas dépasser l'/les unité(s) se trouvant devant elle sauf autorisation ou cas particulier (panne moteur par exemple).""", inline = False)
    embed.add_field(name = "** **", value = """- Lorsqu'une unité se trouve en difficulté (ex : virage raté), elle rejoint la poursuite en laissant d'abord passer TOUTES les unités pour ensuite se réengager en dernière position.""", inline = False)
    embed.add_field(name = "** **", value = """- Les unités Unmarked peuvent rejoindre une poursuite mais elles doivent rester en dernière position. Si une unité Unmarked se trouve face à un refus d'obtempérer ou un délit de fuite elle doit impérativement le signaler en radio, et une fois que des unités sérigraphiées auront rejoint la poursuite, elle leur cède la position et passe en dernière position.""", inline = False)
    embed.add_field(name = "** **", value = """- Une distance de sécurité d'au moins 30m doit être présente entre toutes les unités ainsi que le véhicule suspect. Les véhicules impliqués généralement dans une poursuite de niveau 2 se placent en alternance "gauche/droite" sur la ou les voies disponibles afin d'éviter toute collision entre elles; c'est la configuration dite en quinconce (cf. Image 1).
    ㅤ
    `IMAGE 1`""")
    embed.set_image(url = "https://media.discordapp.net/attachments/541559588659658774/857002631347699742/unknown.png")

    embed2 = discord.Embed(title = "**2. LA MANŒUVRE DU PIT**", color = 0x14C89A)
    embed2.add_field(name = "** **", value = """- Un pit ne peut être effectué que si le traffic et la zone actuelle sont dégagés.""", inline = False)
    embed2.add_field(name = "** **", value = """- Afin de réaliser un pit, il faut au préalable demander l'autorisation en radio au superviseur de patrouille. Si la demande est acceptée, il faut le signaler à toutes les unités présentes sur la poursuite afin qu'elles se préparent à effectuer un rideau.
    __Exemple :___ *1-A-17 effectue un pit une fois que le traffic est dégagé.*""", inline = False)
    embed2.add_field(name = "** **", value = """- Un pit doit être réalisé en priorité par une unité disposant d'une pushbar (par-buffle) et d'une sérigraphie.""", inline = False)
    embed2.add_field(name = "** **", value = """- Lorsqu'on effectue un pit, on ne cogne pas le véhicule cible, on cherche à le pousser afin de le faire partir en tête-à-queue.""", inline = False)
    embed2.add_field(name = "** **", value = """- L'unité ayant effectué un pit continue son chemin afin de bloquer la circulation venant en contre-sens (50-75m) si la route constitue une voie à double-sens. Dans le cas contraire, elle revient auprès des autres unités pour se placer derrière elles en faisant le tour.
    ㅤ
    """, inline = False)
    embed2.add_field(name = "`SCHÉMA 1`", value = "[[PIT]](https://cdn.discordapp.com/attachments/813434903785635887/813449694277533716/pitmanoeuver.mp4)")
    
    embed3 = discord.Embed(title = "**3. Les rideaux**", color = 0x14C89A)
    embed3.add_field(name = "** **", value = """- Un rideau consiste à former un "presque" demi-cercle ou une colonne autour du véhicule suspect lorsque celui-ci est à l'arrêt afin de l'immobiliser et d'interpeller le(s) suspect(s). """, inline = False)
    embed3.add_field(name = "** **", value = """- Si le véhicule possède des dégâts ne lui permettant plus de se dégager, le rideau doit être formé à une distance d'environ 15m (cf. Image 4). Dans le cas contraire, la distance peut-être égale ou inférieure à 5m pour l'immobiliser totalement (cf. Image 3).""", inline = False)
    embed3.add_field(name = "** **", value = """- Les officiers doivent par la suite sortir de leurs véhicules et se placer derrière leurs portières, servant alors de boucliers. Aucun officier ne doit se rapprocher du véhicule suspect seul et sans le signaler aux autres. S'il n'y a pas assez de place pour tous les véhicules, les unités placés l'arrêt à l'arrière descendent de leurs véhicules et rejoignent les unités placés à l'avant.""", inline = False)
    embed3.add_field(name = "** **", value = """- Lorsque le véhicule est immobilisé, il faut ordonner au(x) suspect(s) l'ordre de sortir du véhicule, de garder ses mains en l'air ou derrière la tête et de s'agenouiller.""", inline = False)
    embed3.add_field(name = "** **", value = """- L'approche vers le véhicule doit se réaliser à 2 minimum. S'il y a plus de 4 officiers, 2 s'approchent tandis que les deux autres restent derrière leurs portières en gardant le suspect en joue.
    ㅤ
    `IMAGE 2`""")
    embed3.set_image(url = "https://media.discordapp.net/attachments/541559588659658774/857020703244943380/unknown.png")
    
    embed4 = discord.Embed(title = "** **", color = 0x14C89A)
    embed4.add_field(name = "`IMAGE 3`", value = "** **")
    embed4.set_image(url = "https://media.discordapp.net/attachments/541559588659658774/857036780800835594/unknown.png")

    embed5 = discord.Embed(title = "** **", color = 0x14C89A)
    embed5.add_field(name = "`IMAGE 4`", value = "** **")
    embed5.set_image(url = "https://media.discordapp.net/attachments/541559588659658774/857036847133491260/unknown.png")

    embed6 = discord.Embed(title = "** **", color = 0x14C89A)
    embed6.add_field(name = "`IMAGE 5`", value = "** **")
    embed6.set_image(url = "https://media.discordapp.net/attachments/541559588659658774/857036914653528084/unknown.png")

    await ctx.send(embed = embed)
    time.sleep(1)
    await ctx.send(embed = embed2)
    time.sleep(1)
    await ctx.send(embed = embed3)
    time.sleep(1)
    await ctx.send(embed = embed4)
    time.sleep(1)
    await ctx.send(embed = embed5)
    time.sleep(1)
    await ctx.send(embed = embed6)



# ------------------------------------- #
# Commande pour les annonces police



@bot.command()
async def annonce(ctx):
    if ctx.channel.id == 795567640785190913:
        embed = discord.Embed(title = "**Avis de recherche**", description = "Annonce officielle du département.", color = 0x4D2B2B)
        embed.set_author(name = "Los Santos Police Department", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")   
        embed.add_field(name = "Prime de 50.000$ à offrir !", value = """
        Le département offre une prime de **50.000$** a celui qui pourra prononcer l'arrestation de monsieur **Emiliano Cienfuegos** et le transportera jusque dans nos cellules.
        ㅤ
        Un supplément de **25.000$** sera donné à celui qui arrivera à fournir un enregistrement vidéo et audio des aveux de monsieur **Emiliano Cienfuegos**. 
        ㅤ
        *PS : Ne prenez cependant aucuns risques lors de son arrestation, il est très dangereux et armé jusqu'aux dents. Par conséquents, la prime ne sera déversée si vous ne prenez pas le temps de réclamer du back_up.*
        ㅤ""", inline = False)
        await ctx.send(embed = embed)
        await ctx.send("@everyone`, nouvelle annonce !`")
    else:
        await ctx.send("Attention, tu n'es pas dans le bon salon pour faire cette commande ! \n Vas dans --> <#795567640785190913> ")



# ------------------------------------- #
# Commande pour les annonces police



@bot.command()
async def edit_an(ctx):
    embed = discord.Embed(title = "**Annonce pour le SWAT**", description = "Annonce officielle du département. ***Lisez tout pour les intéressés !!***", color = 0x4D2B2B)
    embed.set_author(name = "Los Santos Police Department", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")   
    embed.add_field(name = "L'annonce est officielle, le SWAT est de retour !", value = """
    Bonjour, vous l'avez sans doute remarqué ces derniers jours, mais le département subit très fréquemment des obligations de faire face à des situations qui parfois peuvent le dépasser.
    ㅤ
    En outre, le Los Santos Police Department ouvre les portes d'une spécialitée, laissée vacante pendant une longue prériode, le **Special Weapon And Tactical** (SWAT).
    Bien entendu, le SWAT aura besoin d'une composition d'officiers les plus compétents et doués avec l'organisation, la coordination avec le chef d'équipe, le maniellement et la connaissance parfaite des armes.
    ㅤ
    Dans un premier temps, nous ne souhaitons recruter que le chef d'équipe de cette unité qui, part la suite, se chargera de mettre en place toutes les disposition relatives aux recrutements.
    ㅤ""", inline = False)
    embed.add_field(name = "`Conditions d'admission :`", value = """
    ㅤ
    - Envoyer une candidature complète expliquant pourquoi vous seriez l'élément idéal pour ce poste et à quel point vous êtes motivé à l'occuper. **L'envoyer au Lieutenant Grants !**
    ㅤ
    - Avoir les grades suivants : **Officer III** ou **Officier III+1**
    ㅤ
    - N'occuper aucune division, si le cas est contraire, vous devrez vous séparer de cette dernière.
    ㅤ
    - Avoir un mental __en acier trempé__ !
    ㅤ
    - Être actif et n'avoir jamais eu d'avertissements ni de suspensions pour un mauvais comportement ou une mise en danger d'un autre officier.
    ㅤ
    ㅤ
    *Nous avons conscience que les conditions imposées sont très exigentes et difficilement obtenables pour certains mais la division du SWAT n'est en rien un jeu et ne peut être occupée que par des éléments qui réunissent toutes ces conditions.*""")
    msg = await bot.get_channel(795567640785190913).fetch_message(857200955682455612)
    await msg.edit(embed = embed)

@bot.command()
async def dispatch(ctx, heure, heure2):
    role = bot.get_guild(859439060552646676).get_role(859559359478759445)
    role2 = bot.get_guild(859439060552646676).get_role(859558445786464277)
    role3 = bot.get_guild(859439060552646676).get_role(859550571341807622)
    if role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
        global msg
        msg = bot.get_channel(859439060552646684)
        embed = discord.Embed(title = "**__Annonce de biefing__**", color = 0x25F3FA)
        embed.set_author(name = "Los Santos Police Dispatch", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")
        embed.add_field(name = f"**Dispatch de __{heure}__** 📋", value = f"""
        ㅤ
        📌 Le briefing de ce jour débutera à `{heure}` précises en salle de dispatch au troisème étage.
        ㅤ
        Veuillez confirmer votre présence, votre absence ou votre retard en utilisant les réactions mises à disposition ci-dessous.
        ㅤ
        ㅤㅤㅤ***• Je serais présent :*** [✅]
        ㅤㅤㅤ***• Je serais absent :*** [❎]
        ㅤㅤㅤ***• Je serais en retard :*** [🕙]
        ㅤ""")
        embed.set_footer(text = "⚠️ Respectez la signification qu'a la réaction que vous avez cochée ! Il ne s'agirait pas de dire que vous êtes présent si vous ne l'êtes pas.")
        axt = await msg.send(embed = embed)
        await axt.add_reaction("✅")
        await axt.add_reaction("❎")
        await axt.add_reaction("🕙")
        await msg.send(f"""<@&863333137152213002>**, nouveau dispatch !** *Veuillez réagir, même absent.*
        ***__Fin des votes à {heure2}__***""")
    else:
        await ctx.send("Vous ne possédez pas les permissions pour faire cela.")


recruitment = 1

@bot.command()
async def nous_rejoindre(ctx):
    msg = bot.get_channel(924360382041161759)
    embed = discord.Embed(title = "**__Nous rejoindre !__**", color = 0x25F3FA)
    embed.set_author(name = "Los Santos Police Department", icon_url = "https://media.discordapp.net/attachments/453268833025785857/834341123177971742/Drapeau.png")
    embed.add_field(name = "Pour rejoindre notre service, vous devrez respecter quelques conditions :", value = f"""
    ㅤ
    ㅤㅤ• Être âgé de 21 ans au minimum 
    ㅤㅤ• Être titulaire du permis de conduire + code
    ㅤㅤ• Avoir le sens de la discipline
    ㅤㅤ• Avoir rédigé une candidature propre, lisible et ***__presque sans fautes__*** (faites 
    ㅤㅤㅤrelire s'il le faut !)
    ㅤㅤ• N'avoir aucuns antécédents judicaires
    ㅤㅤ• Être souvent présent et **être prêt à apprendre**
    ㅤ        
    ⚠️ Si l'une des conditions ci-dessus n'est respectée, d'une quelconque manière, entraînera le refus immédiat de cette candidature.
    ㅤ
    📑 Pour postuler [cliquez ici](https://gtacity-rp.com/lspd/rc.html), les éléments ne devront contenir de fautes d'orthographe (motif de refus si non repsecté).
    ㅤ""")
    
    embed.set_footer(text = "📌 Ouvrir un dossier de candidature signifie que vous êtes prêt à prendre tous les engagements nécessaire pour protéger et servir !")
    global recruitment
    recruitment = await msg.send(embed = embed)
    await ctx.send("Les candidatures sont ouvertues, lisez bien ci-dessus ! <@&924360381407838282>")



number1 = 0
number2 = ""

@bot.event
async def on_raw_reaction_add(payload):
    global number1
    global number2
    if payload.channel_id == 831189253701500999 and payload.message_id == 876441220442914866:
        if payload.member.bot == False:
            if payload.user_id in recruitment.dossiers_liste:
                fm = await bot.get_channel(831189253701500999).fetch_message(876441220442914866)
                await fm.remove_reaction("📩", payload.member)
            if number1 < 10:
                number2 = f"dossier-00{number1}"
                number1 += 1
            elif 9 < number1 < 100:
                number2 = f"dossier-0{number1}"
                number1 += 1
            else:
                number2 = f"dossier-{number1}"
                number1 += 1
            await bot.get_channel(737927401396502538).create_text_channel(name = number2)
            return number1





# ------------------------------------- #     
bot.run("NjU0MzM5MDgzNjgxNzkyMDIw.XfEGwg.if91wcaxJa9pOC_MUxCuUHAcBeU")