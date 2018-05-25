import json
from pandas.io.json import json_normalize
import pandas as pd

with open('static/test.json') as f:
    raw_json = json.load(f)
fps = float(raw_json['framerate'])
timescale = float(raw_json['timescale'])
fragments = pd.DataFrame()

for fi, f in enumerate(raw_json['fragments'] ):
    ff = json_normalize(f)
    ff['fragments_idx'] = fi
    t = ff['start'] /timescale
    events = pd.DataFrame()
    if 'events' in ff.columns:
        for ei, e in enumerate(ff['events'][0]):
            if(e):
                ef = json_normalize(e)
                ef['events_idx'] = ei
                ef['timestamp'] = t
                events = events.append(ef)
            t += ff['interval']/timescale #1/fps
        ff = ff.drop('events',1)
        events['fragments_idx'] = fi
        ff = ff.merge(events, on='fragments_idx', how='outer')
    else:
        t += ff['duration']/timescale
    fragments = fragments.append(ff)

fragments = fragments.reset_index(drop=True)
fragments = fragments.set_index('timestamp')
# next part not working for some reason
fragments.to_json('static/test_result.json')
         #         'height',               'id',
         #   'scores.anger',  'scores.contempt',   'scores.disgust',
         #    'scores.fear', 'scores.happiness',   'scores.neutral',
         # 'scores.sadness',  'scores.surprise',            'start',
         #          'width',                'x',                'y']
