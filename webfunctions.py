import random
import requests
import json
import os
import xml.etree.ElementTree as ET
import asyncio
import aiohttp


def quote():
    baseURL = 'https://animechanapi.xyz/api/quotes/random'
    resp = requests.get(baseURL)
    return resp.json()


def characters(name, page):

    query = '''
    query($search: String){
        Media(search: $search, type: ANIME){
            characters(perPage: 25, page: %d){
                nodes{
                    name{
                        full
                    }
                }
                pageInfo{
                    currentPage
                    lastPage
                    hasNextPage
                }
            }
           
        }
    }


    ''' % (page)

    variables = {
        'search': name
    }

    # Fetching data from anilist api
    base_url1 = 'https://graphql.anilist.co'
    resp1 = requests.post(
        base_url1, json={'query': query, 'variables': variables})
    resp1 = json.loads(resp1.content)

    # return resp1['data']['Media']['characters']['nodes']

    d = {}
    data = []

    for character in resp1['data']['Media']['characters']['nodes']:
        data.append(character['name']['full'])

    if data == []:
        d.update({'characters': ['No characters found for this series']})
    else:
        d.update({
            'characters': data,
            'hasNextPage': resp1['data']['Media']['characters']['pageInfo']['hasNextPage'],
            'currentPage': resp1['data']['Media']['characters']['pageInfo']['currentPage'],
            'lastPage': resp1['data']['Media']['characters']['pageInfo']['lastPage']
        })
    return d


def wallpapers(name):
    name = name.replace(' ', '-')
    baseURL = f"https://wall.alphacoders.com/api2.0/get.php?auth=655421aef6bbbe5ceb5ad3cac13551d6&method=search&term={name}&page=1"
    response = requests.get(baseURL)
    return response.json()


def randomWallpaper(name):
    name = name.replace(' ', '-')
    baseURL = f"https://wall.alphacoders.com/api2.0/get.php?auth=655421aef6bbbe5ceb5ad3cac13551d6&method=search&term={name}&page=1"
    response = requests.get(baseURL)
    response = json.loads(response.content)
    
    if response['total_match'] == '0':
        return 'https://images2.alphacoders.com/710/710137.png'

    result = []
    for wallpaper in response['wallpapers']:
        result.append(wallpaper['url_image'])

    return random.choice(result)


def mal(name):

    name = name.replace(' ', '+')
    base_url = f'https://api.myanimelist.net/v2/anime?q={name}&fields=title,alternative_titles,start_date,end_date,mean,rank,popularity,num_list_users,num_scoring_users,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjljM2RjMzI1YWUxODRjNWRlNGUyYThhNTY4ZjE2ZTRhMGVhMzI0NzU0MTk0M2M4Yjk1ZjNhZjliNWY1NWQ4YWJlMTMyODMyMjdjMjQ2NzEyIn0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjljM2RjMzI1YWUxODRjNWRlNGUyYThhNTY4ZjE2ZTRhMGVhMzI0NzU0MTk0M2M4Yjk1ZjNhZjliNWY1NWQ4YWJlMTMyODMyMjdjMjQ2NzEyIiwiaWF0IjoxNjEzNjM1NTYwLCJuYmYiOjE2MTM2MzU1NjAsImV4cCI6MTYxNjA1MTE1OSwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.BzoqBWKYm_9fd7Oc0dHfPlVWgx6NI_HaSX3WDw9XmSvOdVUTqY-jzEzm3AaGn7RbAAwbErKJh8eLet0QueV3c7axoVS0yG1wg9J-t3c3FmP9xoYIPWigOCqam0-6l3_5tWeAIrFPiQLmiLKwPuMx_dJQYpKFbRran7Zgyx9HD188VkiDXufrOrBn4kXY6lKCP7B8zU6iDwwUc_NBT7Y0d4onPU7TIMy1PE-xqnYzKM6UuHxuJgyeFh7Q3Xhi-gBMJZyjoWh-VwdGn8y5c4I3cCWHOBqxDZZETi2RkL9vSB5vAgM3p7dTHU-Ysdp8bijAEZJa3Co_Jbz3C1y7Fb4lDQ"
    auth = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjljM2RjMzI1YWUxODRjNWRlNGUyYThhNTY4ZjE2ZTRhMGVhMzI0NzU0MTk0M2M4Yjk1ZjNhZjliNWY1NWQ4YWJlMTMyODMyMjdjMjQ2NzEyIn0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjljM2RjMzI1YWUxODRjNWRlNGUyYThhNTY4ZjE2ZTRhMGVhMzI0NzU0MTk0M2M4Yjk1ZjNhZjliNWY1NWQ4YWJlMTMyODMyMjdjMjQ2NzEyIiwiaWF0IjoxNjEzNjM1NTYwLCJuYmYiOjE2MTM2MzU1NjAsImV4cCI6MTYxNjA1MTE1OSwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.BzoqBWKYm_9fd7Oc0dHfPlVWgx6NI_HaSX3WDw9XmSvOdVUTqY-jzEzm3AaGn7RbAAwbErKJh8eLet0QueV3c7axoVS0yG1wg9J-t3c3FmP9xoYIPWigOCqam0-6l3_5tWeAIrFPiQLmiLKwPuMx_dJQYpKFbRran7Zgyx9HD188VkiDXufrOrBn4kXY6lKCP7B8zU6iDwwUc_NBT7Y0d4onPU7TIMy1PE-xqnYzKM6UuHxuJgyeFh7Q3Xhi-gBMJZyjoWh-VwdGn8y5c4I3cCWHOBqxDZZETi2RkL9vSB5vAgM3p7dTHU-Ysdp8bijAEZJa3Co_Jbz3C1y7Fb4lDQ'}

    response = requests.get(base_url, headers=auth)
    # data = json.loads(response.content)
    return response.json()


###################################################### FETCH DETAILS FOR ANIMEINFO PAGE USING ANILIST  #####################################################

def animeInfo_s(name, id):
    query = '''
    query($search: String){
        Media(search: $search, type: ANIME){
            staff{
                edges{
                    role
                }
                nodes{
                    name{
                        full
                    }
                }
            }
            streamingEpisodes{
                title
            }
            characters(perPage: 25){
                edges{
                    role
                }
                nodes{
                    name{
                    full
                    }
                }
            }
            studios{
                nodes{
                    name
                }
            }
        }
    }


    '''

    variables = {
        'search': name
    }
    # Fetching data from anilist api
    base_url1 = 'https://graphql.anilist.co'
    resp1 = requests.post(
        base_url1, json={'query': query, 'variables': variables})
    resp1 = json.loads(resp1.content)

    # Fetching data from Mal api
    base_url2 = f'https://api.myanimelist.net/v2/anime/{id}?fields=title,synopsis,num_episodes'
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw"
    auth = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw'}

    resp2 = requests.get(base_url2, headers=auth)
    resp2 = json.loads(resp2.content)
    d = {}
    # return resp2
    staffs = []
    for staff in resp1['data']['Media']['staff']['nodes']:
        staffs.append(staff['name']['full'])

    roles = []
    for role in resp1['data']['Media']['staff']['edges']:
        roles.append(role['role'])

    staffs = list(zip(staffs, roles))

    episodes = []
    if resp1['data']['Media']['streamingEpisodes'] == []:
        for epi_no in range(1, resp2['num_episodes'] + 1):
            episodes.append(f'Episode - {epi_no}')
    else:
        for episode in resp1['data']['Media']['streamingEpisodes']:
            episodes.append(episode['title'])

    # Characters
    characters = []
    if resp1['data']['Media']['characters']['nodes'] != []:
        for character in resp1['data']['Media']['characters']['nodes']:
            characters.append(character['name']['full'])
    else:
        characters.append(
            "Sorry to inform you but we coudn't fetch any characters list ")

    roles = []
    for role in resp1['data']['Media']['characters']['edges']:
        roles.append(role['role'])

    characters = list(zip(characters, roles))

    studios = []
    for studio in resp1['data']['Media']['studios']['nodes']:
        studios.append(studio['name'])

    d.update({
        'name': resp2['title'],
        'image': resp2['main_picture']['large'],
        'staffs': staffs,
        'episodes': episodes,
        'characters': characters,
        'studios': studios,
        'synopsis': resp2['synopsis'].replace('[Written by MAL Rewrite]', ''),
        'epi_number': resp2['num_episodes']
    })

    d.update({
        'e_number': len(d['episodes']),
        'stu_number': len(d['studios']),
        'stf_number': len(d['staffs']),
        'c_number': len(d['characters'])
    })

    return d


###################################################### FETCH DETAILS FOR ANIMEINFO PAGE USING ANILIST  #####################################################


######################################################## FETCH DETAILS FOR SEARCH PAGE USING MAL + ANN #####################################################

async def fetch_from_mal(name, session):
    name = name.replace(' ', '+')
    base_url = f'https://api.myanimelist.net/v2/anime?q={name}&fields=synopsis'
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw"
    auth = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw'}

    async with session.get(base_url, headers=auth) as resp:
        if resp.status == 200:
            return await resp.text()
        else:
            return


async def main(link):
    # base_link =f'https://cdn.animenewsnetwork.com/encyclopedia/api.xml?title=~{name}'
    base_link = link

    response = requests.get(base_link)
    assets = response.text

    dom = ET.fromstring(assets)
    names = []

    animes = dom.findall('anime')

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*[
            fetch_from_mal(anime.get('name'), session) for anime in animes
        ])

    return results


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def animeInfo(name):
    name = name.replace(' ', '+')
    loop = get_or_create_eventloop()
    fetched_data = loop.run_until_complete(
        main(f'https://cdn.animenewsnetwork.com/encyclopedia/api.xml?title=~{name}'))
    if fetched_data != []:
        for data in fetched_data:
            res = []
            try:
                data = json.loads(data)
                data = data['data']
                for value in data:
                    d = {}
                    d.update({
                        'id': value['node']['id'],
                        'name': value['node']['title'],
                        'image': value['node']['main_picture']['large'],
                        'summary': value['node']['synopsis'].replace('\n\n[Written by MAL Rewrite]', '')
                    })
                    res.append(d)
            except:
                pass
        return res
    else:
        access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw"
        auth = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw'}

        async def mal_rewrite():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.myanimelist.net/v2/anime?q={name}&fields=title,synopsis', headers=auth) as resp:
                    return await resp.text()

        loop = asyncio.get_event_loop()
        fetched_data = json.loads(loop.run_until_complete(mal_rewrite()))
        res = []
        for data in fetched_data:
            try:
                data = fetched_data[data]
                for value in data:
                    d = {}
                    d.update({
                        'id': value['node']['id'],
                        'name': value['node']['title'],
                        'image': value['node']['main_picture']['large'],
                        'summary': value['node']['synopsis'].replace('\n\n[Written by MAL Rewrite]', '')
                    })
                    res.append(d)
            except:
                pass
        return res

######################################################## FETCH DETAILS FOR SEARCH PAGE USING MAL + ANN #####################################################


def accurate_search(name):
    query = '''
        query($search: String){
            Media(search: $search, type: ANIME) {
                        idMal
                title{
                    romaji
                }
                
            }
        }
        '''

    variables = {
        'search': name
    }

    # Fetching data from Anilist
    base_url = 'https://graphql.anilist.co'
    response = requests.post(
        base_url, json={'query': query, 'variables': variables})
    data = json.loads(response.content)

    # Fetching data from MAL
    Id = data['data']['Media']['idMal']
    base_url = f'https://api.myanimelist.net/v2/anime/{Id}?fields=title,synopsis'
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw"
    auth = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5In0.eyJhdWQiOiIzNWU4YWRiMjQ1ODcxYTdiYTUwOWNhZTkzN2JmZDc2OSIsImp0aSI6IjhkNTk0YWQ1MGZjZDFlM2Y5ZGQwNmZjMTA3ODA0YTBkNDI5MjAxOTY2Zjg0ODZmYjNiZDg3NWE5YzMyMmZkODZiYTdmYjgxYzgwNmUxNmM5IiwiaWF0IjoxNjE2MDc3MTY2LCJuYmYiOjE2MTYwNzcxNjYsImV4cCI6MTYxODc1NTU2Niwic3ViIjoiMTE4Mzc1MzMiLCJzY29wZXMiOltdfQ.ahYgUrgJzMeszIWo8IFAQ18cJbduJPv0hr5zbl6RGxxkQiHUEX-vGNR3D-qsloWRh12CN8Z6RA1pb0eYNT4qX5pkwMR0vRTeE-gl4bgi-B-zK-VcHsEks6C_hUMfUhSbYBpOL_8BZy_x4_xs66d2b8aRVQAno1xUPF19BlkJlL9gayGkvQ5PxEjSWH3APC2tLckTbyL-FPzKBX0XWd44EjGwsaUB-Bvs8rqWrvPvXpHhHoKOyK1c9ufw20vEuL3F5B33B2i1WdLDOK87QCvkgnFFyuAnDNJ_ZVb4QsvDYseeI56BW5RFdx-EaaI3iLhk8QRTkZjPV2lLuaCIxlczTw'}

    resp = requests.get(base_url, headers=auth)
    resp = json.loads(resp.content)

    return [{
        'id': resp['id'],
        'name': resp['title'],
        'image': resp['main_picture']['large'],
        'summary': resp['synopsis']
    }]
