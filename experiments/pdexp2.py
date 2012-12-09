import ubiClient as ub

import numpy as np
import pandas as pd
import json

uno = open("12110.json")
uno = uno.read()
uno = pd.DataFrame(json.loads(uno))
uno.sensor = ""
