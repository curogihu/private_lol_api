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

@app.get('/log/big-monster-kill')
def fetch_big_monster_kill():
  base_game_overview_path = os.path.join("D:", os.sep, "output", "game", "timeline", "NA1_*.json")

  file_paths = glob(base_game_overview_path)
  big_monster_kill_log = []

  tmp = []

  killer_logs = []

  for file_path in file_paths[:3]:
    json_data = None

    # print('file_path: ', file_path)

    match_id = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path , 'r') as json_file:
      json_data = json.load(json_file)
      killer_log = []

      for frame in json_data.get('info').get('frames'):
        if not frame.get('events'):
          continue

        for event in frame.get('events'):
          # print('event: ', event.get('type'))
        
          tmp.append(event.get('type'))

          if event.get('type') != 'ELITE_MONSTER_KILL':
            continue

          if event.get('monsterType') == 'DRAGON':
            killer_team_id = event.get('killerTeamId')
            killed_boss_name = event.get('monsterSubType')
            elapsed_match_duration = event.get('timestamp') // 1000

          else:
            killer_team_id = event.get('killerTeamId')
            killed_boss_name = event.get('monsterType')
            elapsed_match_duration = int(event.get('timestamp') // 1000)

            # killer team id will be 300 in case of that herald may be killed by itself.
            if killer_team_id not in [100, 200]:
              continue

          killer_log.append(
            {
              elapsed_match_duration: {
                # 'match_id': os.path.splitext(os.path.basename(file_path))[0],
                'killer_team_id': killer_team_id,
                'killed_boss_name': killed_boss_name,
              }  
            }
          )

    killer_logs.append(
      {
        match_id: killer_log
      }
    )

  return killer_logs

@app.get('/game-duration')
def extract_game_duration():
  base_game_overview_path = os.path.join("D:", os.sep, "output", "game", "info", "NA1_*.json")

  file_paths = glob(base_game_overview_path)
  game_durations = []

  for file_path in tqdm(file_paths):
    json_data = None

    with open(file_path , 'r') as json_file:
      json_data = json.load(json_file)

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
