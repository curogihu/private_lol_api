from match_overview.model import MatchOverview as mo
from glob import glob
from typing import Union
from fastapi import FastAPI

import json
import os

from tqdm import tqdm


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/check")
def value_check():
  # return mo.fetch_game_duration
  pass


@app.get('/game-duration')
def extract_game_duration():
  # base_folder_path = 'D:\output\game\\info'

  base_game_overview_path = os.path.join("D:", os.sep, "output", "game", "info", "NA1_*.json")

  # print('check: ', base_game_overview_path)

  file_paths = glob(base_game_overview_path)
  game_durations = []

  for file_path in tqdm(file_paths):
    # print('file_path: ', file_path)

    json_data = None

    with open(file_path , 'r') as json_file:
      json_data = json.load(json_file)

    # print(json_data)

    game_durations.append(
      {
        'match_id': os.path.splitext(os.path.basename(file_path))[0],
        'game_duration': json_data.get('info', None).get('gameDuration', None)
      }
    )

  return game_durations



'''
type uvicorn main:app --reload

// 20220609093444
// http://127.0.0.1:8000/

{
  "Hello": "World"
}
'''




# if __name__ == '__main__':
#   mo.fetch_game_duration