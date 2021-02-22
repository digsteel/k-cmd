import asyncio

import discord
import os
import random
import json
import time

testMember = []

class MyClient(discord.Client):

    async def on_ready(self):
        print("[QUIZ 1.0.0] Online")

    async def on_message(self, message):
        msg = message.content.split(" ")
        channel = message.channel
        prefix = "!"
        if msg[0] == prefix + "테스트":
            with open("quiz.json", "r") as f:
                data = json.load(f)
            isBan = False
            for i in range(len(data['Ban'])):
                if data['Ban'][i]['ID'] == message.author.id:
                    isBan = True
                    if data['Ban'][i]['Time'] <= time.time():
                        data['Ban'].pop(i)
                        isBan = False
                    break;
            if not isBan:
                for role in message.author.roles:
                    if role.name == "고수":
                        if testMember.count(message.author.id) == 0:
                            testMember.append(message.author.id)
                            if len(data['Challenger']) >= 3:
                                overwrites = {
                                    channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                    message.author: discord.PermissionOverwrite(read_messages=True),
                                    channel.guild.get_member(813409812775567400): discord.PermissionOverwrite(read_messages=True)
                                }

                                channel = await message.guild.create_text_channel(message.author.name , overwrites=overwrites)

                                with open("quiz.json", "r") as f:
                                    data = json.load(f)

                                await channel.send("**\"!시작\"을 입력시 문제가 출제 됩니다.**")

                                def check(m):
                                    return m.content == '!시작' and m.channel == channel and m.author == message.author

                                try:
                                    msg = await client.wait_for('message', timeout=60.0 * 5, check=check)
                                except asyncio.TimeoutError:
                                    await channel.delete()
                                    testMember.remove(message.author.id)
                                    return;

                                correct = 0
                                for i in range(3):
                                    random.shuffle(data['Challenger'])

                                    embed = discord.Embed(
                                        title=str(i + 1) + "번 문제",
                                        description="**" + data['Challenger'][0]['Quiz'] + "**",
                                        colour=discord.Colour.green()
                                    )

                                    await channel.send(content=None, embed=embed)

                                    def check(m):
                                        return m.author == message.author and m.channel == channel

                                    try:
                                        msg = await client.wait_for('message', timeout=90.0, check=check)
                                    except asyncio.TimeoutError:
                                        await channel.send("**시간 초과!**")
                                    else:
                                        if msg.content == data['Challenger'][0]['Answer']:
                                            await channel.send("**정답!**")
                                            correct += 1
                                        else:
                                            await channel.send("**오답!**")
                                    data['Challenger'].pop(0)

                                if correct >= 2:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**승급!**",
                                        colour=discord.Colour.blue()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    await message.author.remove_roles(role)
                                    upRole = discord.utils.get(message.guild.roles, name="고인물")
                                    await message.author.add_roles(upRole)

                                else:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**24시간 동안 재도전 기회 박탈!**",
                                        colour=discord.Colour.red()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    with open("quiz.json", "r") as f:
                                        data = json.load(f)

                                        data['Ban'].append({
                                            "ID": message.author.id,
                                            "Time": time.time() + 86400
                                        })

                                    with open("quiz.json", "w") as f:
                                        json.dump(data, f, indent=4)

                                testMember.remove(message.author.id)
                                startTime = time.time()

                                while True:
                                    if time.time() - startTime >= 5:
                                        await channel.delete()
                                        break;
                                break;
                            else:
                                await channel.send("**해당 등급의 문제가 3개 이상이 아닙니다.**")
                        else:
                            await channel.send("**이미 테스트를 진행중입니다.**")
                    elif role.name == "중수":
                        if testMember.count(message.author.id) == 0:
                            testMember.append(message.author.id)
                            if len(data['GrandMaster']) >= 3:
                                overwrites = {
                                    channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                    message.author: discord.PermissionOverwrite(read_messages=True),
                                    channel.guild.get_member(813409812775567400): discord.PermissionOverwrite(
                                        read_messages=True)
                                }

                                channel = await message.guild.create_text_channel(message.author.name,
                                                                                  overwrites=overwrites)

                                with open("quiz.json", "r") as f:
                                    data = json.load(f)

                                await channel.send("**\"!시작\"을 입력시 문제가 출제 됩니다.**")

                                def check(m):
                                    return m.content == '!시작' and m.channel == channel and m.author == message.author

                                try:
                                    msg = await client.wait_for('message', timeout=60.0 * 5, check=check)
                                except asyncio.TimeoutError:
                                    await channel.delete()
                                    testMember.remove(message.author.id)
                                    return;

                                correct = 0
                                for i in range(3):
                                    random.shuffle(data['GrandMaster'])

                                    embed = discord.Embed(
                                        title=str(i + 1) + "번 문제",
                                        description="**" + data['GrandMaster'][0]['Quiz'] + "**",
                                        colour=discord.Colour.green()
                                    )

                                    await channel.send(content=None, embed=embed)

                                    def check(m):
                                        return m.author == message.author and m.channel == channel

                                    try:
                                        msg = await client.wait_for('message', timeout=90.0, check=check)
                                    except asyncio.TimeoutError:
                                        await channel.send("**시간 초과!**")
                                    else:
                                        if msg.content == data['GrandMaster'][0]['Answer']:
                                            await channel.send("**정답!**")
                                            correct += 1
                                        else:
                                            await channel.send("**오답!**")
                                    data['GrandMaster'].pop(0)

                                if correct >= 2:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**승급!**",
                                        colour=discord.Colour.blue()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    await message.author.remove_roles(role)
                                    upRole = discord.utils.get(message.guild.roles, name="고수")
                                    await message.author.add_roles(upRole)

                                else:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**24시간 동안 재도전 기회 박탈!**",
                                        colour=discord.Colour.red()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    with open("quiz.json", "r") as f:
                                        data = json.load(f)

                                        data['Ban'].append({
                                            "ID": message.author.id,
                                            "Time": time.time() + 86400
                                        })

                                    with open("quiz.json", "w") as f:
                                        json.dump(data, f, indent=4)

                                testMember.remove(message.author.id)
                                startTime = time.time()

                                while True:
                                    if time.time() - startTime >= 5:
                                        await channel.delete()
                                        break;
                                break;
                            else:
                                await channel.send("**해당 등급의 문제가 3개 이상이 아닙니다.**")
                        else:
                            await channel.send("**이미 테스트를 진행중입니다.**")
                    elif role.name == "초보":
                        if testMember.count(message.author.id) == 0:
                            testMember.append(message.author.id)
                            if len(data['Master']) >= 3:
                                overwrites = {
                                    channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                    message.author: discord.PermissionOverwrite(read_messages=True),
                                    channel.guild.get_member(813409812775567400): discord.PermissionOverwrite(
                                        read_messages=True)
                                }

                                channel = await message.guild.create_text_channel(message.author.name,
                                                                                  overwrites=overwrites)

                                with open("quiz.json", "r") as f:
                                    data = json.load(f)

                                await channel.send("**\"!시작\"을 입력시 문제가 출제 됩니다.**")

                                def check(m):
                                    return m.content == '!시작' and m.channel == channel and m.author == message.author

                                try:
                                    msg = await client.wait_for('message', timeout=60.0 * 5, check=check)
                                except asyncio.TimeoutError:
                                    await channel.delete()
                                    testMember.remove(message.author.id)
                                    return;

                                correct = 0
                                for i in range(3):
                                    random.shuffle(data['Master'])

                                    embed = discord.Embed(
                                        title=str(i + 1) + "번 문제",
                                        description="**" + data['Master'][0]['Quiz'] + "**",
                                        colour=discord.Colour.green()
                                    )

                                    await channel.send(content=None, embed=embed)

                                    def check(m):
                                        return m.author == message.author and m.channel == channel

                                    try:
                                        msg = await client.wait_for('message', timeout=90.0, check=check)
                                    except asyncio.TimeoutError:
                                        await channel.send("**시간 초과!**")
                                    else:
                                        if msg.content == data['Master'][0]['Answer']:
                                            await channel.send("**정답!**")
                                            correct += 1
                                        else:
                                            await channel.send("**오답!**")
                                    data['Master'].pop(0)

                                if correct >= 2:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**승급!**",
                                        colour=discord.Colour.blue()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    await message.author.remove_roles(role)
                                    upRole = discord.utils.get(message.guild.roles, name="중수")
                                    await message.author.add_roles(upRole)

                                else:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**24시간 동안 재도전 기회 박탈!**",
                                        colour=discord.Colour.red()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    with open("quiz.json", "r") as f:
                                        data = json.load(f)

                                        data['Ban'].append({
                                            "ID": message.author.id,
                                            "Time": time.time() + 86400
                                        })

                                    with open("quiz.json", "w") as f:
                                        json.dump(data, f, indent=4)

                                testMember.remove(message.author.id)
                                startTime = time.time()

                                while True:
                                    if time.time() - startTime >= 5:
                                        await channel.delete()
                                        break;
                                break;
                            else:
                                await channel.send("**해당 등급의 문제가 3개 이상이 아닙니다.**")
                        else:
                            await channel.send("**이미 테스트를 진행중입니다.**")
                    elif role.name == "뉴비":
                        if testMember.count(message.author.id) == 0:
                            testMember.append(message.author.id)
                            if len(data['Beginner']) >= 3:
                                overwrites = {
                                    channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                    message.author: discord.PermissionOverwrite(read_messages=True),
                                    channel.guild.get_member(813409812775567400): discord.PermissionOverwrite(
                                        read_messages=True)
                                }

                                channel = await message.guild.create_text_channel(message.author.name,
                                                                                  overwrites=overwrites)

                                with open("quiz.json", "r") as f:
                                    data = json.load(f)

                                await channel.send("**\"!시작\"을 입력시 문제가 출제 됩니다.**")

                                def check(m):
                                    return m.content == '!시작' and m.channel == channel and m.author == message.author

                                try:
                                    msg = await client.wait_for('message', timeout=60.0 * 5, check=check)
                                except asyncio.TimeoutError:
                                    await channel.delete()
                                    testMember.remove(message.author.id)
                                    return;

                                correct = 0
                                for i in range(3):
                                    random.shuffle(data['Beginner'])

                                    embed = discord.Embed(
                                        title=str(i + 1) + "번 문제",
                                        description="**" + data['Beginner'][0]['Quiz'] + "**",
                                        colour=discord.Colour.green()
                                    )

                                    await channel.send(content=None, embed=embed)

                                    def check(m):
                                        return m.author == message.author and m.channel == channel

                                    try:
                                        msg = await client.wait_for('message', timeout=90.0, check=check)
                                    except asyncio.TimeoutError:
                                        await channel.send("**시간 초과!**")
                                    else:
                                        if msg.content == data['Beginner'][0]['Answer']:
                                            await channel.send("**정답!**")
                                            correct += 1
                                        else:
                                            await channel.send("**오답!**")
                                    data['Beginner'].pop(0)

                                if correct >= 2:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**승급!**",
                                        colour=discord.Colour.blue()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    await message.author.remove_roles(role)
                                    upRole = discord.utils.get(message.guild.roles, name="초보")
                                    await message.author.add_roles(upRole)

                                else:
                                    embed = discord.Embed(
                                        title="결과",
                                        description="**24시간 동안 재도전 기회 박탈!**",
                                        colour=discord.Colour.red()
                                    )
                                    embed.add_field(name="**맞힌 문제 수**", value=str(correct), inline=True)

                                    await channel.send(content=None, embed=embed)

                                    with open("quiz.json", "r") as f:
                                        data = json.load(f)

                                        data['Ban'].append({
                                            "ID": message.author.id,
                                            "Time": time.time() + 86400
                                        })

                                    with open("quiz.json", "w") as f:
                                        json.dump(data, f, indent=4)

                                testMember.remove(message.author.id)
                                startTime = time.time()

                                while True:
                                    if time.time() - startTime >= 5:
                                        await channel.delete()
                                        break;
                                break;
                            else:
                                await channel.send("**해당 등급의 문제가 3개 이상이 아닙니다.**")
                        else:
                            await channel.send("**이미 테스트를 진행중입니다.**")
            else:
                await channel.send("**재도전 기회 박탈 기간이 만료되지 않았습니다.**")
        elif msg[0] == prefix + "문제":
            if msg[1] == "리스트":
                if len(msg) > 2:
                    if msg[2] == "초보":
                        with open("quiz.json", "r") as f:
                            data = json.load(f)

                        if len(data['Beginner']) == 0:
                            await channel.send("**등록된 문제가 없습니다**")
                            return

                        s = ""
                        for i in range(len(data['Beginner'])):
                            s += str(i+1) + "번 | " + data['Beginner'][i]['Quiz'] + " | " + data['Beginner'][i]['Answer'] + "\n"

                        embed = discord.Embed(
                            title="초보 문제 리스트",
                            description="**"+s+"**",
                            colour=discord.Colour.gold()
                        )

                        await channel.send(content=None, embed=embed)
                    elif msg[2] == "중수":
                        with open("quiz.json", "r") as f:
                            data = json.load(f)

                        if len(data['Beginner']) == 0:
                            await channel.send("**등록된 문제가 없습니다**")
                            return

                        s = ""
                        for i in range(len(data['Master'])):
                            s += str(i+1) + "번 | " + data['Master'][i]['Quiz'] + " | " + data['Master'][i]['Answer'] + "\n"

                        embed = discord.Embed(
                            title="중수 문제 리스트",
                            description="**"+s+"**",
                            colour=discord.Colour.gold()
                        )

                        await channel.send(content=None, embed=embed)
                    elif msg[2] == "고수":
                        with open("quiz.json", "r") as f:
                            data = json.load(f)

                        if len(data['Beginner']) == 0:
                            await channel.send("**등록된 문제가 없습니다**")
                            return

                        s = ""
                        for i in range(len(data['GrandMaster'])):
                            s += str(i+1) + "번 | " + data['GrandMaster'][i]['Quiz'] + " | " + data['GrandMaster'][i]['Answer'] + "\n"

                        embed = discord.Embed(
                            title="고수 문제 리스트",
                            description="**"+s+"**",
                            colour=discord.Colour.gold()
                        )

                        await channel.send(content=None, embed=embed)
                    elif msg[2] == "고인물":
                        with open("quiz.json", "r") as f:
                            data = json.load(f)

                        if len(data['Beginner']) == 0:
                            await channel.send("**등록된 문제가 없습니다**")
                            return

                        s = ""
                        for i in range(len(data['Challenger'])):
                            s += str(i+1) + "번 | " + data['Challenger'][i]['Quiz'] + " | " + data['Challenger'][i]['Answer'] + "\n"

                        embed = discord.Embed(
                            title="고인물 문제 리스트",
                            description="**"+s+"**",
                            colour=discord.Colour.gold()
                        )

                        await channel.send(content=None, embed=embed)
                    else:
                        await channel.send("**존재하지 않는 등급입니다.**")
                else:
                    await channel.send("**등급을 입력해주세요.**")
            elif msg[1] == "등록":
                if len(msg) > 2:
                    if msg[2] == "초보":
                        snt = message.content.split("\"")

                        if len(snt) > 4:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['Beginner'].append({
                                "Quiz": snt[1],
                                "Answer": snt[3]
                            })

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 등록했습니다.**")
                        else:
                            await channel.send("**문제나 답을 작성해주세요.**")
                    elif msg[2] == "중수":
                        snt = message.content.split("\"")

                        if len(snt) > 4:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['Master'].append({
                                "Quiz": snt[1],
                                "Answer": snt[3]
                            })

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 등록했습니다.**")
                        else:
                            await channel.send("**문제나 답을 작성해주세요.**")
                    elif msg[2] == "고수":
                        snt = message.content.split("\"")

                        if len(snt) > 4:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['GrandMaster'].append({
                                "Quiz": snt[1],
                                "Answer": snt[3]
                            })

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 등록했습니다.**")
                        else:
                            await channel.send("**문제나 답을 작성해주세요.**")
                    elif msg[2] == "고인물":
                        snt = message.content.split("\"")

                        if len(snt) > 4:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['Challenger'].append({
                                "Quiz" : snt[1],
                                "Answer": snt[3]
                            })

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 등록했습니다.**")
                        else:
                            await channel.send("**문제나 답을 작성해주세요.**")
                    else:
                        await channel.send("**존재하지 않는 등급입니다.**")
                else:
                    await channel.send("**등급을 입력해주세요.**")
            elif msg[1] == "삭제":
                if len(msg) > 2:
                    if msg[2] == "초보":
                        if len(msg) > 3:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['Beginner'].pop(int(msg[3])-1)

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 삭제했습니다.**")
                        else:
                            await channel.send("**삭제할 문제 번호를 입력해 주세요.**")
                    elif msg[2] == "중수":
                        if len(msg) > 3:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['Master'].pop(int(msg[3])-1)

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 삭제했습니다.**")
                        else:
                            await channel.send("**삭제할 문제 번호를 입력해 주세요.**")
                    elif msg[2] == "고수":
                        if len(msg) > 3:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['GrandMaster'].pop(int(msg[3])-1)

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 삭제했습니다.**")
                        else:
                            await channel.send("**삭제할 문제 번호를 입력해 주세요.**")
                    elif msg[2] == "고인물":
                        if len(msg) > 3:
                            with open("quiz.json", "r") as f:
                                data = json.load(f)

                            data['Challenger'].pop(int(msg[3])-1)

                            with open("quiz.json", "w") as f:
                                json.dump(data, f, indent=4)

                            await channel.send("**문제를 삭제했습니다.**")
                        else:
                            await channel.send("**삭제할 문제 번호를 입력해 주세요.**")
                    else:
                        await channel.send("**존재하지 않는 등급입니다.**")
                else:
                    await channel.send("**등급을 입력해주세요.**")
        elif msg[0] == prefix + "풀기":
            if len(message.mentions) <= 1:
                with open("quiz.json", "r") as f:
                    data = json.load(f)

                for i in range(len(data['Ban'])):
                    if data['Ban'][i]['ID'] == message.mentions[0].id:
                        data['Ban'].pop(i)

                with open("quiz.json", "w") as f:
                    json.dump(data, f, indent=4)

                await channel.send("**해당 유저를 페널티를 풀었습니다.**")
            else:
                await channel.send("**언급을 한명만 해주세요.**")


access_token = os.environ["BOT_TOKEN"]       
client = MyClient()
client.run(access_token)
