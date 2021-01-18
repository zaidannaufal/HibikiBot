import discord
from discord.ext import commands
import asyncio
from jikanpy import Jikan

class Searchanime(commands.Cog):
    
    def __init__(self, client):
        self.client = client
       
    @commands.command(aliases=['ani','a','anime'])
    async def animesearch(self,ctx,*,anime):
        jikan = Jikan()
        search = jikan.search('anime', anime, page=1)
        search_res = search['results']
        if anime == search_res[0]['title']:
            await ctx.send(embed=animedetails(search_res[0]['mal_id']))
        else:
            ani = "** Please select an Anime with 1-5: **\n"  
            malid = []         
            for i in range(5):
                ani = ani + f"**{i+1}.** {search_res[i]['title']}\n"
                malid.append(search_res[i]['mal_id'])
            
            await ctx.send(ani)

            def check(message):
                return message.author == ctx.author and (int(message.content)) >=1 and (int(message.content)) <=5 

            try:
                message = await self.client.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                await ctx.send(embed=animedetails(malid[int(message.content)-1])) 
        
        


def airing(start,end):
    month = {'01': 'Jan',
             '02' : 'Feb',
             '03' : 'March',
             '04': 'Apr',
             '05' : 'May',
             '06' : 'June',
             '07': 'July',
             '08' : 'Aug',
             '09' : 'Sept',
             '10': 'Oct',
             '11' : 'Nov',
             '12' : 'Dec'}
    if not end:
        return f"{month[start[5:7]]} {start[8:10]}, {start[:4]} to -"
    elif not end and not start:
        return "unknown"
    else:
        return f"{month[start[5:7]]} {start[8:10]}, {start[:4]} to {month[end[5:7]]} {end[8:10]},{end[:4]}"  
    
def othername(synonym):
    othername = ' '
    if not synonym:
        othername = '-'
    else:
        count = len(synonym) 
        for i in range (count-1):
            othername += synonym[i] + ', '
        othername += synonym[count-1] + '.'
    return othername

def studio(studios):
    result = ''
    if not studios:
        return '-'
    else :
        for s in studios:
            result = result + s['name'] + " "
        return result

def song(anime):
    result = ''
    if not anime:
        return '-'
    else:
        for s in anime:
            result = result + s + '\n'
        return result
    
# def studio(anime):
#     studio = ''
#     list_studio = anime.studios
#     if not list_studio:
#         studio = '-'
#     else:
#         count = len(list_studio)
#         for i in range (count-1):
#             studio += f'{list_studio[i]}, '
#         studio += f'{list_studio[count-1]}'
#     return studio
def animedetails(anime):
        jikan = Jikan()
        ani = jikan.anime(anime)
        embed=discord.Embed(title= ani['title'], 
                            url=ani['url'], 
                            description= f"Othername: {othername(ani['title_synonyms'])}", 
                            color=0x2746a5)
        embed.set_image(url=ani['image_url'])
        embed.add_field(name="Type", value=ani['type'] , inline=True)
        embed.add_field(name="Episode", value=ani['episodes'], inline=True)
        embed.add_field(name="Aired", value=ani['aired']['string'], inline=True)
        embed.add_field(name="Score", value=ani['score'], inline=True)
        embed.add_field(name="Studios", value=studio(ani['studios']), inline=True)
        embed.add_field(name="Source", value=ani['source'], inline=True)
        embed.add_field(name="Opening Themes", value=song(ani['opening_themes']), inline=True)
        embed.add_field(name="Ending Themes", value=song(ani['ending_themes']), inline=True)
        # embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')
        return embed
 
def setup(client):
    client.add_cog(Searchanime(client))

