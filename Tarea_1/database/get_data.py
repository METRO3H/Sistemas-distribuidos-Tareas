import requests
import time
import sqlite3

start = time.time()
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

query = '''
query ($page: Int) {
   
  Page(page: $page){
     media(type: ANIME) {
       id
      title {
        romaji
      }
      source
     }
    pageInfo {
      currentPage
      hasNextPage
    }
  }

}
'''

variables = {
    'page': 1
}

url = 'https://graphql.anilist.co'

sql_insert = "INSERT INTO anime (id, title, source) VALUES (?, ?, ?)"
hasNextPage = True
iterator = 1

while(hasNextPage):
    
  try:
      variables["page"] = iterator
      
      response = requests.post(url, json={'query': query, 'variables': variables})
      response.raise_for_status()

      data = response.json()
      page = data['data']['Page']
      media_dataset = page['media']
      page_info = page['pageInfo']
      current_page = page_info['currentPage']

      print("Page", current_page, "=>", len(media_dataset), "elements")
      
      dataset = []
      for media in media_dataset:
            data_tuple = (media['id'], media['title']['romaji'], media["source"])
            dataset.append(data_tuple)

      cursor.executemany(sql_insert, dataset)
      conn.commit()
      
      if page_info['hasNextPage'] != hasNextPage:
          hasNextPage = False
      iterator += 1
      time.sleep(3)
  except requests.exceptions.RequestException as e:
      print('Error making request:', e)
      break
  



# Cerrar la conexión
conn.close()

end = time.time()

print("El proceso se ha demorado ", end - start, "segundos")