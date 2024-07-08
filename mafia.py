import asyncio
import operator
import discord
import random
import os
import configparser
import shutil
import time
import datetime

intents = discord.Intents.default()

while True:
    client = discord.Client(intents=intents)

    option = configparser.ConfigParser()
    option.read("setting.ini", encoding="utf-8")
    prefix = option["setting"]["prefix"]
    token = option["setting"]["token"]

    try:
        shutil.rmtree("log")
        time.sleep(.0000000000000001)
    except:
        pass
    os.makedirs("log")


    @client.event
    async def on_ready():
        print("Logged in as ")
        print(client.user.id)
        print("made by sexybaby")
        print("===========")
        game = discord.Game(prefix + "마피아도움말")
        await client.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(3600)
        while True:
            if os.listdir("log") == []:
                await client.logout()
                break
            await asyncio.sleep(60)


    @client.event
    async def on_reaction_add(reaction, user):
        a = 0
        try:
            if os.path.isfile("log/" + str(reaction.message.guild.id) + ".ini"):
                if str(reaction.emoji) in ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '👍', '👎']:
                    a = 3
                else:
                    a = 2
        except:
            pass

        if a == 2:
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name="마피아채널")
            system = configparser.ConfigParser()
            system.read("log/" + str(reaction.message.guild.id) + ".ini", encoding="utf-8")
            mem = await guild.fetch_member(int(user.id))
            if system["info"]["time"] == "낮":
                if user.id != client.user.id and str(reaction.emoji) == "❌" and str(user.id) not in str(system["info"]["dead"]):
                    while True:
                        system = configparser.ConfigParser()
                        system.read("log/" + str(reaction.message.guild.id) + ".ini", encoding="utf-8")
                        if str(user.id) not in system["info"]["skipman"]:
                            pass
                        else:
                            break

                    if system["info"]["skipman"].count(str(user.id)) == 1:
                        if int(system["info"]["skipnum"]) > int(system["info"]["currentp"]) * 0.5:
                            await reaction.message.channel.send("과반수의 스킵으로 저녁으로 넘어갑니다.")
                        else:
                            await reaction.message.channel.send("`" + user.name + "` 님의 스킵요청 (" + system["info"]["skipnum"] + "/" + str(int(int(system["info"]["currentp"]) * 0.5) + 1) + ")")

                    else:
                        await reaction.message.channel.send("`" + user.name + "` 이미 스킵요청 했습니다.")

                elif user.id != client.user.id and str(reaction.emoji) == "⏰" and role in mem.roles:
                    if str(user.id) not in system["info"]["extension"]:
                        system["info"]["extension"] = system["info"]["extension"] + str(user.id) + "/"
                        system["info"]["debate"] = str(int(system["info"]["debate"]) + 1)

                        file = open("log/" + str(reaction.message.guild.id) + ".ini", "w", encoding="utf-8")
                        system.write(file)
                        file.close()

                        await reaction.message.channel.send("`" + user.name + "` 님의 연장신청")
                    else:
                        await reaction.message.channel.send("`" + user.name + "` 이미 연장했습니다.")

        elif a == 3:
            role = discord.utils.get(reaction.message.guild.roles, name="마피아채널")
            if role not in user.roles and user != client.user:
                await reaction.remove(user)

    @client.event
    async def on_message(message):
        if isinstance(message.channel, discord.abc.PrivateChannel):
            try:
                if 1 <= int(message.content) <= 8:
                    pass
                else:
                    return
            except:
                return

            content = ""
            async for msg in message.author.history(limit=10):
                if "죽일 사람을" in msg.content or "살릴 사람을" in msg.content or "조사할 사람을" in msg.content:
                    content = msg.content
                    break

            num = int(message.content) + 1
            line = content.split("\n")
            guild = line[1].split("(")[1].split(")")[0]
            guild = await client.fetch_guild(int(guild))
            kp = line[num].split("(")[-1].split(")")[0]
            kplayer = await guild.fetch_member(int(kp))
            role = discord.utils.get(guild.roles, name="마피아채널")

            mem = await guild.fetch_member(int(message.author.id))
            if role in mem.roles:
                pass
            else:
                return

            system = configparser.ConfigParser()
            system.read("log/" + str(guild.id) + ".ini", encoding="utf-8")

            async def heal(user):
                if system["info"][str(user.id)] == "의사":
                    if system["info"]["time"] == "밤":
                        if role in kplayer.roles:
                            if str(user.id) != kp:
                                system["info"]["saveperson"] = kp
                                file = open("log/" + str(guild.id) + ".ini", "w", encoding="utf-8")
                                system.write(file)
                                file.close()
                                if kplayer.nick is None:
                                    await user.send(
                                        "======================================\n`" + kplayer.name + "`님을 살립니다.")
                                else:
                                    await user.send(
                                        "======================================\n`" + kplayer.name + "[" + kplayer.nick + "]`님을 살립니다.")
                            else:
                                await user.send("======================================\n자기 자신을 살릴 수 없습니다.")
                        else:
                            await user.send("======================================\n올바른 대상자가 아닙니다.")
                    else:
                        await user.send("======================================\n밤이 아닙니다.")

                else:
                    await user.send("======================================\n당신이 의사가 아닙니다.")

            async def find(user):
                if system["info"][str(user.id)] == "경찰":
                    if system["info"]["time"] == "밤":
                        if role in kplayer.roles:
                            if system["info"]["look"] == "-":
                                if system["info"][kp] == "마피아":
                                    if kplayer.nick is None:
                                        await user.send(
                                            "======================================\n`" + kplayer.name + "`님은 마피아가 맞습니다")
                                    else:
                                        await user.send(
                                            "======================================\n`" + kplayer.name + "[" + kplayer.nick + "]`님은 마피아가 맞습니다")
                                else:
                                    if kplayer.nick is None:
                                        await user.send(
                                            "======================================\n`" + kplayer.name + "`님은 마피아가 아닙니다")
                                    else:
                                        await user.send(
                                            "======================================\n`" + kplayer.name + "[" + kplayer.nick + "]`님은 마피아가 아닙니다")
                                system["info"]["look"] = "1"
                                file = open("log/" + str(guild.id) + ".ini", "w", encoding="utf-8")
                                system.write(file)
                                file.close()
                            else:
                                await user.send("======================================\n오늘밤 이미 확인하셨습니다.")
                        else:
                            await user.send("======================================\n올바른 대상자가 아닙니다.")
                    else:
                        await user.send("======================================\n밤이 아닙니다.")
                else:
                    await user.send("======================================\n당신이 경찰이 아닙니다.")

            async def kill(user):
                if system["info"][str(user.id)] == "마피아":
                    if system["info"]["time"] == "밤":
                        if role in kplayer.roles:
                            if system["info"][kp] != "마피아":
                                system["info"]["killperson"] = kp
                                file = open("log/" + str(guild.id) + ".ini", "w", encoding="utf-8")
                                system.write(file)
                                file.close()
                                if kplayer.nick is None:
                                    await user.send(
                                        "======================================\n`" + kplayer.name + "`님을 죽입니다")
                                else:
                                    await user.send(
                                        "======================================\n`" + kplayer.name + "[" + kplayer.nick + "]`님울 죽입니다")
                            else:
                                await user.send("======================================\n마피아는 죽일 수 없습니다.")
                        else:
                            await user.send("======================================\n올바른 대상자가 아닙니다.")
                    else:
                        await user.send("======================================\n밤이 아닙니다.")
                else:
                    await user.send("======================================\n당신이 마피아가 아닙니다.")

            if message.author.id != client.user.id and "죽일 사람을" in content:
                await kill(message.author)

            elif message.author.id != client.user.id and "살릴 사람을" in content:
                await heal(message.author)

            elif message.author.id != client.user.id and "조사할 사람을" in content:
                await find(message.author)

        if message.content.startswith(prefix + "마피아도움말"):
            des0 = "내 이름? 그런것은 알 필요 없다.\n어둠이 내리면 우리는 모두 같아지지...\n\u200b"
            des1 = ("1. 봇을 초대한다."
                    "\n2. 초대시 봇에게 부여되는 권한은 게임진행에 꼭 필요함"
                    "\n3. `" + prefix + "마피아생성` 으로 채널과 역할 생성"
                                        "\n4. 참가할 멤버들은 모두 DM 허용해야함"
                                        "\n5. 게임인원은 4~7인\n\u200b")

            des2 = ("1. `" + prefix + "수동시작` `유저아이디` `유저아이디2` `...`\n\u200b")

            des3 = ("1. `마피아대기실` 접속"
                    "\n2. `" + prefix + "자동시작`\n\u200b")

            des4 = ("1. 밤이 되면 직업(`마피아`, `의사`, `경찰`, `영매`)을 가진 사람은 봇과의 DM을 통해 활동한다."
                    "\n\n2. `마피아`는 서로 상의하여 죽일 사람을 선택\n`의사`는 살릴 사람을 선택\n`경찰`은 누군가가 마피아인지 조사\n`영매`는 전날 처형당한 사람 마피아인지 확인"
                    "\n\n3. `밤`에는 채널에서 `채팅,대화금지`"
                    "\n\n4. 마피아가 이틀 연속으로 아무도 죽이지 않으면 게임이 종료된다."
                    "\n\n5. `낮`에는 `토론` 후 의심가는 사람에게 투표"
                    "\n\n6. 가장 많이 지목된 사람의 `최후변론`"
                    "\n\n7. 살릴지 죽일지 `최종투표`한다.\n살려가 죽여보다 많다면 대상자는 풀려나고\n그 반대의 경우는 처형"
                    "\n\n8. 시민의 수가 마피아의 수와 같아지면 마피아의 승리, 마피아가 모두 죽으면 시민의 승리\n\u200b")

            maker = ("게임중인 채널내에서\n`" + prefix + "게임종료`\n\u200b")

            me = ("[초대 및 공지](https://discord.gg/MmtSCYxQnp)"
                  "\n" + str(len(client.guilds)) + "개의 서버에서 이용중" 
                  "\n제작자 <@722371670936911982>\n\u200b")

            embed = discord.Embed(color=0x26b4df)
            embed.add_field(name="소개", value=des0, inline=False)
            embed.add_field(name="준비(관리자)", value=des1, inline=False)
            embed.add_field(name="수동시작", value=des2)
            embed.add_field(name="자동시작", value=des3)
            embed.add_field(name="게임방법", value=des4, inline=False)
            embed.add_field(name="강제종료", value=maker)
            embed.add_field(name="출처", value=me)
            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(
                icon_url="https://postfiles.pstatic.net/MjAxOTA0MThfMiAg/MDAxNTU1NTI1NTQzNTIz.0EsAcCWsfNB4yE7YlDVTASb5cE-O0yLZyXZBjV9WEoQg.beOMwtvVCGZpshta0L1f7PyTujElPUkMXK674-L2nPEg.PNG.gkje123/mapia.png",
                text="팀베이비")
            await message.channel.send(embed=embed)

        if message.content.startswith(prefix + "마피아생성") and not isinstance(message.channel, discord.abc.PrivateChannel):
            if not message.author.guild_permissions.administrator:
                await message.channel.send("당신이 서버의 관리자가 아닙니다.")
                return

            if discord.utils.get(message.guild.channels, name="마피아채널") is not None or discord.utils.get(message.guild.roles, name="마피아채널") is not None or discord.utils.get(message.guild.channels, name="마피아채널 보이스") is not None or discord.utils.get(message.guild.channels, name="마피아대기실") is not None:
                await message.channel.send("이미 같은 이름의 채널이나 역할이 존재합니다.")
                return

            try:
                c = await message.guild.create_text_channel(name="마피아채널")
                v = await message.guild.create_voice_channel(name="마피아채널 보이스")
                await message.guild.create_voice_channel(name="마피아대기실")
                m = await message.guild.create_role(name="마피아채널", hoist=True)
                d = await message.guild.create_role(name="마피아무덤", hoist=True)
                me = await message.guild.fetch_member(745849612996313139)

                mev = discord.PermissionOverwrite(connect=True, speak=True)
                await v.set_permissions(me, overwrite=mev)
                mec = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                await c.set_permissions(me, overwrite=mec)

                everyv = discord.PermissionOverwrite(connect=False)
                await v.set_permissions(message.guild.default_role, overwrite=everyv)
                everyc = discord.PermissionOverwrite(read_messages=False)
                await c.set_permissions(message.guild.default_role, overwrite=everyc)

                voice = discord.PermissionOverwrite(connect=True, speak=True)
                await v.set_permissions(m, overwrite=voice)
                chat = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                await c.set_permissions(m, overwrite=chat)

                dv = discord.PermissionOverwrite(connect=True, speak=False)
                await v.set_permissions(d, overwrite=dv)
                dc = discord.PermissionOverwrite(read_messages=True, send_messages=False)
                await c.set_permissions(d, overwrite=dc)
            except:
                await message.channel.send("봇에게 필요한 역할이 없습니다. 초대코드에 있는 역할을 모두 부여해주세요.")

        if message.content.startswith(prefix + "게임종료"):
            if os.path.isfile("log/" + str(message.guild.id) + ".ini") and message.channel.name == "마피아채널":
                pass
            else:
                return

            try:
                await message.channel.send("게임을 종료합니다.")

                system = configparser.ConfigParser()
                system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")
                mem = system["info"]["player"]
                mem = mem.split(" ")
                playerlist = [await message.guild.fetch_member(int(m)) for m in mem]

                vchannel = discord.utils.get(message.guild.channels, name="마피아채널 보이스")
                grave = discord.utils.get(message.guild.channels, name="마피아대기실")
                role = discord.utils.get(message.guild.roles, name="마피아채널")
                dead = discord.utils.get(message.guild.roles, name="마피아무덤")

                for player in playerlist:
                    try:
                        await player.remove_roles(role)
                    except:
                        pass

                for player in playerlist:
                    try:
                        await player.remove_roles(dead)
                    except:
                        pass

                for cm in vchannel.members:
                    try:
                        await cm.edit(voice_channel=grave)
                    except:
                        pass
            except:
                pass

            os.remove("log/" + str(message.guild.id) + ".ini")

        if message.content.startswith(prefix + "자동시작"):
            if os.path.isfile("log/" + str(message.guild.id) + ".ini"):
                await message.channel.send("이미 서버에서 마피아 게임이 진행중입니다.")
                return
            else:
                file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                file.write("[info]")
                file.close()

            grave = discord.utils.get(message.guild.channels, name="마피아대기실")
            vchannel = discord.utils.get(message.guild.channels, name="마피아채널 보이스")
            channel = discord.utils.get(message.guild.channels, name="마피아채널")
            role = discord.utils.get(message.guild.roles, name="마피아채널")

            if grave is None or vchannel is None or channel is None or role is None:
                await message.channel.send("마피아채널 및 역할이 없습니다. /마피아생성으로 채널과 역할을 만들어주세요.")
                os.remove("log/" + str(message.guild.id) + ".ini")
                return

            if len(grave.members) < 4 or len(grave.members) > 7:
                await message.channel.send("마피아대기실(보이스채널)에 시작가능한 인원(4~7)이 없습니다.")
                os.remove("log/" + str(message.guild.id) + ".ini")
                return

            await message.channel.send(prefix + "시작 " + " ".join([str(m.id) for m in grave.members]))

        if message.content.startswith(prefix + "수동시작"):
            if os.path.isfile("log/" + str(message.guild.id) + ".ini"):
                await message.channel.send("이미 서버에서 마피아 게임이 진행중입니다.")
                return
            else:
                file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                file.write("[info]")
                file.close()

            grave = discord.utils.get(message.guild.channels, name="마피아대기실")
            vchannel = discord.utils.get(message.guild.channels, name="마피아채널 보이스")
            channel = discord.utils.get(message.guild.channels, name="마피아채널")
            role = discord.utils.get(message.guild.roles, name="마피아채널")
            mem = message.content[6:]
            memls = mem.split(" ")

            if grave is None or vchannel is None or channel is None or role is None:
                await message.channel.send("마피아채널 및 역할이 없습니다. /마피아생성으로 채널과 역할을 만들어주세요.")
                os.remove("log/" + str(message.guild.id) + ".ini")
                return

            if len(memls) > 7 or len(memls) < 4:
                await message.channel.send("게임참가자의 아이디를 4~7인으로 입력해주세요.")
                os.remove("log/" + str(message.guild.id) + ".ini")
                return

            await message.channel.send(prefix + "시작 " + mem)

        ########################################################################################################################################################

        if message.content.startswith(prefix + "시작") and message.author == client.user:
            channel = discord.utils.get(message.guild.channels, name="마피아채널")
            grave = discord.utils.get(message.guild.channels, name="마피아대기실")
            role = discord.utils.get(message.guild.roles, name="마피아채널")
            dead = discord.utils.get(message.guild.roles, name="마피아무덤")
            vchannel = discord.utils.get(message.guild.channels, name="마피아채널 보이스")
            mem = message.content[4:]
            mem = mem.split(" ")
            dielist = []
            try:
                playerlist = [await message.guild.fetch_member(int(m)) for m in mem]
                dmlist = [await message.guild.fetch_member(int(m)) for m in mem]
            except:
                await message.channel.send("유저아이디 및 띄어쓰기가 올바른 양식인지 확인해주세요")
                return

            try:
                for player in playerlist:
                    await player.send("======================================\nDM테스트 중입니다.")
            except:
                if player.nick is None:
                    await message.channel.send(player.name + "님 DM을 푸시지요. 죽고싶습니까?")
                else:
                    await message.channel.send(player.name + "[" + player.nick + "]님 DM을 푸시지요. 죽고싶습니까?")
                os.remove("log/" + str(message.guild.id) + ".ini")
                return

            if len(mem) == 4:
                list = ["시민", "시민", "시민", "마피아"]
            elif len(mem) == 5:
                list = ["시민", "시민", "시민", "경찰", "마피아"]
            elif len(mem) == 6:
                list = ["시민", "시민", "경찰", "의사", "마피아", "마피아"]
            elif len(mem) == 7:
                list = ["시민", "시민", "영매", "경찰", "의사", "마피아", "마피아"]
            else:
                await message.channel.send("마피아 게임이 가능한 인원이 아닙니다. 4~7인으로 시작해주세요.")
                os.remove("log/" + str(message.guild.id) + ".ini")
                return

            try:
                try:
                    msg = []
                    async for m in channel.history():
                        msg.append(m)
                    await channel.delete_messages(msg)
                except:
                    pass

                for m in role.members:
                    await m.remove_roles(role)

                for m in dead.members:
                    await m.remove_roles(dead)

                for m in vchannel.members:
                    await m.edit(voice_channel=grave)

                for player in playerlist:
                    await player.add_roles(role)

                for player in playerlist:
                    try:
                        await player.edit(voice_channel=vchannel)
                    except:
                        pass
            except:
                await message.channel.send("봇에게 필요한 역할이 없습니다. 초대코드에 있는 역할을 모두 부여해주세요.")
                os.remove("log/" + str(message.guild.id) + ".ini")
                return

            await message.channel.send("DM테스트 완료. <#" + str(channel.id) + ">에서 게임을 시작합니다.")

            random.shuffle(list)

            system = configparser.ConfigParser()
            system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

            system["info"]["player"] = message.content[4:]
            system["info"]["startp"] = str(len(mem))
            system["info"]["currentp"] = str(len(mem))
            system["info"]["dead"] = ""
            system["info"]["mafia"] = str(list.count("마피아"))
            system["info"]["citizen"] = str(len(mem) - list.count("마피아"))

            file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
            system.write(file)
            file.close()

            exitcount = 0
            job = []

            greet = "마피아 게임을 시작합니다. DM으로 직업을 배분합니다."

            if len(mem) == 4:
                await channel.send(greet + "\n이번 게임의 직업은 `시민 3`, `마피아 1` 입니다.")
            elif len(mem) == 5:
                await channel.send(greet + "\n이번 게임의 직업은 `시민 3`, `경찰 1`, `마피아 1` 입니다.")
            elif len(mem) == 6:
                await channel.send(greet + "\n이번 게임의 직업은 `시민 2`, `경찰 1`, `의사 1`, `마피아 2` 입니다.")
            elif len(mem) == 7:
                await channel.send(greet + "\n이번 게임의 직업은 `시민 2`, `경찰 1`, `의사 1`, `영매 1`, `마피아 2` 입니다.")

            mm = 0
            map1 = ""

            for i in range(len(mem)):
                system = configparser.ConfigParser()
                system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                system["info"][mem[i]] = list[i]

                file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                system.write(file)
                file.close()

                member = await message.guild.fetch_member(int(mem[i]))
                if member.nick is None:
                    job.append(member.name + " : " + list[i])
                else:
                    job.append(member.name + "[" + member.nick + "] : " + list[i])
                await member.send("==============<#" + str(channel.id) + ">==============\n당신의 직업은 `" + list[
                    i] + "`입니다.\n마피아들은 서로를 확인해주세요 5초 후 게임이 시작됩니다...")
                if list[i] == "마피아" and mm == 0:
                    map1 = member
                    mm = 1
                elif list[i] == "마피아" and mm == 1:
                    map2 = member
                    await map1.send("또 다른 마피아는 <@" + str(map2.id) + ">님 입니다.")
                    await map2.send("또 다른 마피아는 <@" + str(map1.id) + ">님 입니다.")

            system = configparser.ConfigParser()
            system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

            system["info"]["hangman"] = "-"

            file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
            system.write(file)
            file.close()

            await asyncio.sleep(5)

            ########################################################################################################################################################
            while True:
                try:
                    shutup = discord.PermissionOverwrite(connect=True, speak=False)
                    nwrite = discord.PermissionOverwrite(read_messages=True, send_messages=False)
                    await vchannel.set_permissions(role, overwrite=shutup)
                    await channel.set_permissions(role, overwrite=nwrite)

                    system = configparser.ConfigParser()
                    system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                    system["info"]["time"] = "밤"
                    system["info"]["killperson"] = "-"
                    system["info"]["saveperson"] = "-"
                    system["info"]["look"] = "-"

                    file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                    system.write(file)
                    file.close()

                    for m in dmlist:
                        if system["info"][str(m.id)] == "마피아":
                            msg = "==============<#" + str(channel.id) + ">==============\n```죽일 사람을 선택하세요.(" + str(
                                message.guild.id) + ")"
                            for i in range(len(dmlist)):
                                if dmlist[i].nick is None:
                                    msg = msg + "\n" + str(i + 1) + ". " + dmlist[i].name + " (" + str(
                                        dmlist[i].id) + ")"
                                else:
                                    msg = msg + "\n" + str(i + 1) + ". " + dmlist[i].name + "[" + dmlist[
                                        i].nick + "] (" + str(dmlist[i].id) + ")"
                            ms = await m.send(msg + "```")

                        elif system["info"][str(m.id)] == "의사":
                            msg = "==============<#" + str(channel.id) + ">==============\n```살릴 사람을 선택하세요.(" + str(
                                message.guild.id) + ")"
                            for i in range(len(dmlist)):
                                if dmlist[i].nick is None:
                                    msg = msg + "\n" + str(i + 1) + ". " + dmlist[i].name + " (" + str(
                                        dmlist[i].id) + ")"
                                else:
                                    msg = msg + "\n" + str(i + 1) + ". " + dmlist[i].name + "[" + dmlist[
                                        i].nick + "] (" + str(dmlist[i].id) + ")"
                            ms = await m.send(msg + "```")

                        elif system["info"][str(m.id)] == "경찰":
                            msg = "==============<#" + str(channel.id) + ">==============\n```조사할 사람을 선택하세요.(" + str(
                                message.guild.id) + ")"
                            for i in range(len(dmlist)):
                                if dmlist[i].nick is None:
                                    msg = msg + "\n" + str(i + 1) + ". " + dmlist[i].name + " (" + str(
                                        dmlist[i].id) + ")"
                                else:
                                    msg = msg + "\n" + str(i + 1) + ". " + dmlist[i].name + "[" + dmlist[
                                        i].nick + "] (" + str(dmlist[i].id) + ")"
                            ms = await m.send(msg + "```")

                        elif system["info"][str(m.id)] == "영매":
                            if system["info"]["hangman"] == "-":
                                await m.send(
                                    "==============<#" + str(channel.id) + ">==============\n지난낮 사형당한 사람이 없습니다.")
                            else:
                                hang = await message.guild.fetch_member(int(system["info"]["hangman"]))
                                if hang.nick is None:
                                    await m.send("======================================<#" + str(
                                        channel.id) + ">\n지난낮 사형당한 " + hang.name + "님의 영혼과 접선합니다...")
                                else:
                                    await m.send("======================================<#" + str(
                                        channel.id) + ">\n지난낮 사형당한 " + hang.name + "[" + hang.nick + "]님의 영혼과 접선합니다...")
                                await asyncio.sleep(2)
                                if system["info"][str(hang.id)] == "마피아":
                                    await m.send(":ghost: 그래 내가 바로 마피아다 크크크...")
                                else:
                                    await m.send(":ghost: 난 마피아가 아니야!! 억울해..흑흑")

                    await channel.send("======================================\n<@&" + str(role.id) + "> 밤이 되었습니다.")
                    await channel.send(file=discord.File("pic/night.jpg"))
                    await channel.send("`40초` 동안 마피아, 의사, 경찰이 움직입니다."
                                       "\n자세한 사항은 해당 직업인에게 DM으로 보내집니다.")

                    await asyncio.sleep(40)

                    system = configparser.ConfigParser()
                    system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                    system["info"]["time"] = "아침"

                    file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                    system.write(file)
                    file.close()

                    speak = discord.PermissionOverwrite(connect=True, speak=True)
                    write = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    await channel.set_permissions(role, overwrite=write)
                    await vchannel.set_permissions(role, overwrite=speak)

                    if system["info"]["killperson"] == "-":
                        exitcount += 1
                        if exitcount == 2:
                            await channel.send(
                                "======================================\n두번 연속으로 마피아가 아무도 죽이지 않았습니다."
                                "\n잠수로 판단되어 게임을 종료합니다. 5초 뒤 방이 터집니다.")

                            await asyncio.sleep(5)

                            for m in dmlist:
                                try:
                                    await m.remove_roles(role)
                                except:
                                    pass

                            for m in dielist:
                                try:
                                    await m.remove_roles(dead)
                                except:
                                    pass

                            for cm in vchannel.members:
                                try:
                                    await cm.edit(voice_channel=grave)
                                except:
                                    pass

                            for player in playerlist:
                                try:
                                    await player.send("```" + "\n".join(job) + "```")
                                except:
                                    pass

                            os.remove("log/" + str(message.guild.id) + ".ini")

                            return

                        await channel.send(
                            "======================================\n<@&" + str(role.id) + "> 아침이 되었습니다.")
                        await channel.send("지난밤 아무도 죽지 않았습니다."
                                           "\n두번 연속으로 마피아가 아무도 죽이지 않으면 게임이 자동 종료됩니다.")

                    elif system["info"]["killperson"] != "-" and system["info"]["killperson"] == system["info"][
                        "saveperson"]:
                        await channel.send(
                            "======================================\n<@&" + str(role.id) + "> 아침이 되었습니다.")
                        await channel.send("지난밤 누군가가 죽을뻔 했으나 의사가 살렸습니다.")

                    else:
                        diemem = await message.guild.fetch_member(int(system["info"]["killperson"]))
                        await channel.send(
                            "======================================\n<@&" + str(role.id) + "> 아침이 되었습니다.")
                        if diemem.nick is None:
                            await channel.send("지난밤 `" + diemem.name + "`님이 죽었습니다.")
                        else:
                            await channel.send("지난밤 `" + diemem.name + "[" + diemem.nick + "]`님이 죽었습니다.")

                        try:
                            system = configparser.ConfigParser()
                            system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")
                            system["info"]["dead"] = system["info"]["dead"] + " " + str(diemem.id)
                            file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                            system.write(file)
                            file.close()
                            await diemem.remove_roles(role)
                            await diemem.add_roles(dead)
                        except:
                            pass

                        dmlist.remove(diemem)
                        dielist.append(diemem)

                        await diemem.send("======================================\n당신은 마피아에게 주것습니다.")

                        system = configparser.ConfigParser()
                        system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                        system["info"]["currentp"] = str(int(system["info"]["currentp"]) - 1)
                        if system["info"][system["info"]["killperson"]] == "마피아":
                            system["info"]["mafia"] = str(int(system["info"]["mafia"]) - 1)
                        else:
                            system["info"]["citizen"] = str(int(system["info"]["citizen"]) - 1)

                        file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                        system.write(file)
                        file.close()

                        if int(system["info"]["mafia"]) >= int(system["info"]["citizen"]):
                            await channel.send("======================================\n마피아의 수와 시민의 수가 같아졌습니다."
                                               "\n:spy: **마피아의 승리**입니다"
                                               "\n게임이 종료되었습니다. `5초` 후 방이 터집니다.")

                            await asyncio.sleep(5)

                            for m in dmlist:
                                try:
                                    await m.remove_roles(role)
                                except:
                                    pass

                            for m in dielist:
                                try:
                                    await m.remove_roles(dead)
                                except:
                                    pass

                            for cm in vchannel.members:
                                try:
                                    await cm.edit(voice_channel=grave)
                                except:
                                    pass

                            for player in playerlist:
                                try:
                                    await player.send("```" + "\n".join(job) + "```")
                                except:
                                    pass

                            os.remove("log/" + str(message.guild.id) + ".ini")

                            return

                        elif int(system["info"]["mafia"]) == 0:
                            await channel.send("======================================\n마피아가 모두 죽었습니다."
                                               "\n:family_wwg: **시민의 승리**입니다"
                                               "\n게임이 종료되었습니다. `5초` 후 방이 터집니다.")

                            await asyncio.sleep(5)

                            for m in dmlist:
                                try:
                                    await m.remove_roles(role)
                                except:
                                    pass

                            for m in dielist:
                                try:
                                    await m.remove_roles(dead)
                                except:
                                    pass

                            for cm in vchannel.members:
                                try:
                                    await cm.edit(voice_channel=grave)
                                except:
                                    pass

                            for player in playerlist:
                                try:
                                    await player.send("```" + "\n".join(job) + "```")
                                except:
                                    pass

                            os.remove("log/" + str(message.guild.id) + ".ini")

                            return

                    await asyncio.sleep(2)
                    await channel.send("======================================\n<@&" + str(role.id) + "> 낮이 되었습니다.")
                    await channel.send(file=discord.File("pic/morning.jpg"))

                    system = configparser.ConfigParser()
                    system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                    system["info"]["time"] = "낮"
                    system["info"]["extension"] = "/"
                    system["info"]["skipman"] = "/"
                    system["info"]["debate"] = system["info"]["currentp"]
                    system["info"]["skipnum"] = "0"

                    file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                    system.write(file)
                    file.close()

                    a = await channel.send(
                        "`" + str(int(system["info"]["currentp"]) * 15) + "초` 동안 자유롭게 대화해주세요.(⏰:시간연장 ❌:스킵)")
                    await a.add_reaction("⏰")
                    await a.add_reaction("❌")

                    def check(react, user):
                        system = configparser.ConfigParser()
                        system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")
                        if str(react.emoji) == "❌" and user.id != client.user.id and str(user.id) not in str(system["info"]["dead"]):
                            if os.path.isfile("log/" + str(react.message.guild.id) + ".ini"):
                                system = configparser.ConfigParser()
                                system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")
                                if str(user.id) not in system["info"]["skipman"]:
                                    system["info"]["skipman"] = system["info"]["skipman"] + str(user.id) + "/"
                                    system["info"]["skipnum"] = str(int(system["info"]["skipnum"]) + 1)

                                    file = open("log/" + str(react.message.guild.id) + ".ini", "w", encoding="utf-8")
                                    system.write(file)
                                    file.close()

                                    if int(system["info"]["skipnum"]) > int(system["info"]["currentp"]) * 0.5:
                                        return True
                                else:
                                    system["info"]["skipman"] = system["info"]["skipman"] + str(user.id) + "/"

                                    file = open("log/" + str(react.message.guild.id) + ".ini", "w", encoding="utf-8")
                                    system.write(file)
                                    file.close()

                    time = 0
                    while True:
                        time += 1
                        try:
                            await client.wait_for("reaction_add", check=check, timeout=15)
                            break
                        except:
                            pass

                        system = configparser.ConfigParser()
                        system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                        sett = int(system["info"]["debate"])

                        a = await channel.send("**<" + str(time * 15) + "/" + str(sett * 15) + "초 경과>**")
                        await a.add_reaction("⏰")
                        await a.add_reaction("❌")

                        if sett == time:
                            break
                        else:
                            pass

                    system = configparser.ConfigParser()
                    system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                    system["info"]["time"] = "재판"

                    file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                    system.write(file)
                    file.close()

                    await channel.send("======================================\n<@&" + str(role.id) + "> 저녁이 되었습니다.")
                    await channel.send("재판대에 올릴 사람을 정해주세요(제한시간 : `10초`)")

                    namelist = []
                    idlist = []
                    n = 0
                    playerlist = [await message.guild.fetch_member(p.id) for p in playerlist]
                    for player in playerlist:
                        if role in player.roles:
                            n += 1
                            if player.nick is None:
                                namelist.append(str(n) + ". " + player.name)
                            else:
                                namelist.append(str(n) + ". " + player.name + "[" + player.nick + "]")
                            idlist.append(player.id)

                    votelist = await channel.send("```" + "\n".join(namelist) + "```")
                    vnls = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
                    for i in range(10):
                        if len(idlist) >= i + 1:
                            await votelist.add_reaction(vnls[i])

                    await asyncio.sleep(10)

                    vls = {}
                    votelist = discord.utils.get(client.cached_messages, id=votelist.id)
                    for i in range(len(idlist)):
                        for reaction in votelist.reactions:
                            if str(reaction.emoji) == vnls[i]:
                                cnt = 0
                                us = await reaction.users().flatten()
                                for u in us:
                                    mem = await message.guild.fetch_member(u.id)
                                    if role in mem.roles:
                                        cnt += 1
                                vls[i] = cnt

                    vls = sorted(vls.items(), key=operator.itemgetter(1), reverse=True)

                    if vls[0][1] == vls[1][1]:
                        system = configparser.ConfigParser()
                        system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                        system["info"]["hangman"] = "-"

                        file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                        system.write(file)
                        file.close()

                        await channel.send("동점입니다. 부결로 재판이 종료됩니다.")

                    else:
                        winner = idlist[vls[0][0]]
                        winner = await message.guild.fetch_member(int(winner))
                        if winner.nick is None:
                            await channel.send("희생자 : `" + winner.name + "`")
                        else:
                            await channel.send("희생자 : `" + winner.name + "[" + winner.nick + "]`")
                        await channel.send(
                            "======================================\n`" + winner.name + "`님 최후변론의 시간입니다(제한시간 : `15초`)")
                        await asyncio.sleep(15)

                        votems = await channel.send("======================================\n살려? 죽여? (제한시간 : `10초`)")
                        await votems.add_reaction('👍')
                        await votems.add_reaction('👎')

                        await asyncio.sleep(10)

                        votems = discord.utils.get(client.cached_messages, id=votems.id)

                        c1 = 0
                        c2 = 0

                        for reaction in votems.reactions:
                            if str(reaction.emoji) == '👍':
                                cnt = 0
                                us = await reaction.users().flatten()
                                for u in us:
                                    mem = await message.guild.fetch_member(u.id)
                                    if role in mem.roles:
                                        cnt += 1
                                c1 = cnt
                            elif str(reaction.emoji) == '👎':
                                cnt = 0
                                us = await reaction.users().flatten()
                                for u in us:
                                    mem = await message.guild.fetch_member(u.id)
                                    if role in mem.roles:
                                        cnt += 1
                                c2 = cnt

                        if c1 > c2:
                            await channel.send("살립니다.")
                            system = configparser.ConfigParser()
                            system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")

                            system["info"]["hangman"] = "-"

                            file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                            system.write(file)
                            file.close()

                        else:
                            await channel.send("죽입니다.")
                            diemem = winner
                            try:
                                system = configparser.ConfigParser()
                                system.read("log/" + str(message.guild.id) + ".ini", encoding="utf-8")
                                system["info"]["dead"] = system["info"]["dead"] + " " + str(diemem.id)
                                file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                                system.write(file)
                                file.close()
                                await diemem.remove_roles(role)
                                await diemem.add_roles(dead)
                            except:
                                pass

                            dmlist.remove(diemem)
                            dielist.append(diemem)

                            await diemem.send("======================================\n당신은 처형당했습니다.")

                            await channel.send("**<처형완료>**")

                            system["info"]["hangman"] = str(diemem.id)
                            system["info"]["currentp"] = str(int(system["info"]["currentp"]) - 1)

                            if system["info"][str(diemem.id)] == "마피아":
                                system["info"]["mafia"] = str(int(system["info"]["mafia"]) - 1)
                            else:
                                system["info"]["citizen"] = str(int(system["info"]["citizen"]) - 1)

                            file = open("log/" + str(message.guild.id) + ".ini", "w", encoding="utf-8")
                            system.write(file)
                            file.close()

                            if int(system["info"]["mafia"]) >= int(system["info"]["citizen"]):
                                await channel.send(
                                    "======================================\n마피아의 수와 시민의 수가 같아졌습니다."
                                    "\n:spy: **마피아의 승리**입니다"
                                    "\n게임이 종료되었습니다. `5초` 후 방이 터집니다.")

                                await asyncio.sleep(5)

                                for m in dmlist:
                                    try:
                                        await m.remove_roles(role)
                                    except:
                                        pass

                                for m in dielist:
                                    try:
                                        await m.remove_roles(dead)
                                    except:
                                        pass

                                for cm in vchannel.members:
                                    try:
                                        await cm.edit(voice_channel=grave)
                                    except:
                                        pass

                                for player in playerlist:
                                    try:
                                        await player.send("```" + "\n".join(job) + "```")
                                    except:
                                        pass

                                os.remove("log/" + str(message.guild.id) + ".ini")

                                return

                            elif int(system["info"]["mafia"]) == 0:
                                await channel.send("======================================\n마피아가 모두 죽었습니다."
                                                   "\n:family_wwg: **시민의 승리**입니다"
                                                   "\n게임이 종료되었습니다. `5초` 후 방이 터집니다.")

                                await asyncio.sleep(5)

                                for m in dmlist:
                                    try:
                                        await m.remove_roles(role)
                                    except:
                                        pass

                                for m in dielist:
                                    try:
                                        await m.remove_roles(dead)
                                    except:
                                        pass

                                for cm in vchannel.members:
                                    try:
                                        await cm.edit(voice_channel=grave)
                                    except:
                                        pass

                                for player in playerlist:
                                    try:
                                        await player.send("```" + "\n".join(job) + "```")
                                    except:
                                        pass

                                os.remove("log/" + str(message.guild.id) + ".ini")

                                return

                except:
                    for m in dmlist:
                        try:
                            await m.remove_roles(role)
                        except:
                            pass

                    for m in dielist:
                        try:
                            await m.remove_roles(dead)
                        except:
                            pass

                    for cm in vchannel.members:
                        try:
                            await cm.edit(voice_channel=grave)
                        except:
                            pass

                    for player in playerlist:
                        try:
                            await player.send("```" + "\n".join(job) + "```")
                        except:
                            pass

                    os.remove("log/" + str(message.guild.id) + ".ini")

                    return


    client.loop.run_until_complete(client.start("토큰"))