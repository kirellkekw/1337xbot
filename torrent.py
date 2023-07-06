import nextcord
from nextcord.ext.commands.context import Context
from nextcord.ext import commands
import requests
import json
from py1337x import py1337x
from main import prefix
import asyncio


class Torrent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx: Context, *, query):
        torrents = py1337x()
        results = torrents.search(query, sortBy='seeders')["items"]
        embed = nextcord.Embed(
            title=f"Torrents for \"{query}\"", color=nextcord.Color.random())
        if len(results) == 0:
            embed.add_field(name="No results found",
                            value="Try another search term")
            await ctx.send(embed=embed)
            return
        for result in results:
            _ = "name"
            embed.add_field(
                name=f"(**{result['size']}**) {result[_] if len(result[_]) < 60 else f'{result[_][0:60]}...'}",
                value=f"Click [here]({result['link']}) to go to download page\nOr type `{prefix}info {result['torrentId']}` for more info"
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx: Context, *, query):
        torrents = py1337x()
        results = torrents.info(torrentId=query)
        apiUrl = "https://tormag.ezpz.work/api/api.php?action=insertMagnets"
        data = {"magnets":
                [
                results["magnetLink"]
                ]
                }
        res = requests.post(apiUrl, json=data)
        responseJson = json.loads(res.text)
        if "magnetEntries" in responseJson:
            links = responseJson["magnetEntries"]
            if links:
                maglink:str = links[0]
        else:
            maglink:str = responseJson["message"]

        name = results['shortName'] if results['shortName'] else results['name']

        embed = nextcord.Embed(title=f"(**{results['size']}**) {name}",
                               description=f"[magnet link]({maglink})", color=nextcord.Color.random())
        if results['description'] != None:
            embed.add_field(name='description', value=results['description'])
        embed.add_field(name='category', value=results['category'])
        embed.add_field(name='language', value=results['language'])
        embed.add_field(name="seeders/leechers",
                        value=f"{results['seeders']}/{results['leechers']}")
        embed.add_field(name="downloads", value=results['downloads'])
        embed.add_field(name="uploader", value=results['uploader'])
        embed.add_field(name="upload date", value=results['uploadDate'])
        
        if results['thumbnail'] != None:
            embed.set_thumbnail(url=results['thumbnail'])
        elif results['images'][0] != None:
            embed.set_thumbnail(url=results['images'][0])

        await ctx.send(embed=embed)

    @commands.command()
    async def trending(self, ctx: Context):
        torrents = py1337x()
        results = torrents.trending()['items']
        asyncio.sleep(1)
        print(results)
        embed = nextcord.Embed(
            title="Trending torrents", color=nextcord.Color.random())
        for result in results[0:12]:
            _ = "name"
            embed.add_field(
                name=f"(**{result['size']}**) {result[_] if len(result[_]) < 60 else f'{result[_][0:60]}...'}",
                value=f"Click [here]({result['link']}) to go to download page\nOr type `{prefix}info {result['torrentId']}` for more info"
            )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Torrent(bot))
