import discord

setup_start = discord.Embed(description="Willkommen auf unserem Elektrotechnik Discord Server!\n\n"
                                        "Dieses Setup ist dafür da, damit wir und deine Kommilitonen "
                                        "dich auf dem Server "
                                        "(besser) erkennen und du zu deiner Gruppe passende Informationen erhältst.\n\n"
                                        "*Deine Angaben werden von diesem Bot weder gespeichert noch auf irgeindeine "
                                        "Weise verarbeitet, du erhältst ledeglich deinen Namen und deine Studiengruppe "
                                        "auf unserem Server zugewiesen.*\n\n"
                                        "**Antworte bitte mit deinem Vor- und Nachnamen auf diese Nachricht**\n"
                                        "_Wenn du deinen vollen Namen hier nicht angeben willst, "
                                        "darfst du auch nur deinen Vornamen benutzen._",
                            colour=discord.Colour(0x2fb923),
                            title="Setup")

setup_name_error = discord.Embed(description="Hoppla!\n"
                                             "Dein eingegebener Name ist zu lang.\n"
                                             "Gehe Sicher, dass deine Eingabe nicht länger als 32 Zeichen ist.",
                                 colour=discord.Colour(0x2fb923),
                                 title="Setup")


def setup_group_select(name, semesters):
    embed = discord.Embed(description=f'Hallo **{name}**!\n'
                                      f'Antworte jetzt noch mit deiner Studiengruppe, '
                                      f'um dieses Setup abzuschließen.\n\n'
                                      f'**Folgende Studiengruppen stehen zur Auswahl:**\n',
                          colour=discord.Colour(0x2fb923),
                          title="Setup")

    # add embed_fields acording to semester and groups
    for semester in semesters:
        group_string = ''
        for group in semester.groups:
            group_string += str(group) + '\n'
        embed.add_field(name=str(semester), value=group_string, inline=True)
    return embed


def setup_group_error(message):
    embed = discord.Embed(description=f'Hoppla!\n'
                                      f'Wie es scheint, ist {message} keine gültige Studiengruppe.\n'
                                      f'Probiere es bitte nochmal mit einer Studiengruppe aus der Liste!\n'
                                      f'Ist deine Studiengruppe nicht dabei?\n'
                                      f'Dann kontaktiere bitte einen Admin (mit rotem Namen auf dem Server)!',
                          colour=discord.Colour(0x2fb923),
                          title="Setup")
    return embed


def setup_end(study_group_name):
    embed = discord.Embed(description=f'Vielen Dank für die Einschreibung in unseren EIT-Server.\n'
                                      f'Du wurdest der Studiengruppe **{study_group_name}** zugewiesen.\n\n'
                                      f'Hiermit hast du das Setup abgeschlossen und deine Angaben\n'
                                      f'werden in den Server eingetragen.\n\n'
                                      f'__Falls etwas mit deiner Eingabe nicht stimmt,\n'
                                      f'führe bitte einfach nochmal das Setup aus und pass deine Eingabe an!__',
                          colour=discord.Colour(0x2fb923),
                          title="Setup")
    return embed


def add_quicklinks(embed):
    embed.add_field(name="__Quicklinks:__",
                    value="*[HM-Startseite](https://www.hm.edu/)*   |  "
                          "*[FK 04](https://www.ee.hm.edu/aktuelles/stundenplaene/schwarzesbrett.de.html)*   |  "
                          "*[Moodle](https://moodle.hm.edu/my)*   |  "
                          "*[Primuss](https://www3.primuss.de/cgi-bin/login/index.pl?FH=fhm)*")
    return embed
