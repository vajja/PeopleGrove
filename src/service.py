import re
import string

import numpy as np
from nltk.corpus import stopwords

from src import *
from src.utils.logger_utils import Logger
from src.utils.model_utils import LoadModel

LOGGER = Logger.get_instance()


class Service:
    replace_data = ["master of science in", "bachelor of science in", "master of science", "bachelor of science",
                    "bachelors in", "bachelor's in", "bachelors", "masters in", "master's in", "masters",
                    "bs in", "ms in", "ms", "m.s in", "m.s", "b.s in", "b.s", "bs in", "bs", "bachelor of arts", "gpa",
                    "bba", "b.b.a", "mba", "m.b.a", "b.a", "ba", "major in", "major", "minor in", "minor",
                    "concentration in", "concentration", "master's", "masters", "bachelor's", "bachelors",
                    "n/a", "master", "bachelor", "degree", "certificate"]
    stop_words = set(stopwords.words('english'))

    @classmethod
    def clean(cls, data):
        val = data.strip()
        out = []
        if val != "":
            if val.endswith('.'):
                val = val[:-1]
            if val == "n/a":
                val = ""
            temp = val.split()
            while val and val[0] not in string.ascii_letters:
                val = val[1:]
            while val and val[-1] not in string.ascii_letters:
                val = val[:-1]
            val = " ".join(temp)
            val = val.lower()
            val = val.strip()
            val = val.replace(" w/ ", " and ")
            val = val.replace("&", "and")
            val = val.replace("/", " ")
            val = val.replace("-", " ")
            val = re.sub('[^A-Z^a-z^0-9^\s]+', '', val)
            temp = val.split()
            temp = [e.strip() for e in temp]
            val = " ".join(temp)
            for d in cls.replace_data:
                if val.startswith(d + " ") or " " + d + " " in val or val.endswith(" " + d):
                    val = val.replace(d + " ", "")
                    val = val.strip()
                    while val and val[0] not in string.ascii_letters:
                        val = val[1:]
                    temp = val.split()
                    temp = [e.strip() for e in temp]
                    if len(temp) > 1:
                        while temp and temp[0] in cls.stop_words:
                            temp.pop(0)
                        while temp and temp[-1] in cls.stop_words:
                            temp.pop()
                        val = " ".join(temp)
                val = " ".join(temp)
            while val and val[0] not in string.ascii_letters:
                val = val[1:]
            while val and val[-1] not in string.ascii_letters:
                val = val[:-1]
            val = val.strip()
            val = val.split()
            for v in val:
                if v not in cls.stop_words and len(v) > 2:
                    out.append(v)
            return out
        return out

    @classmethod
    def match_logic(cls, a, b):
        match = 0
        if len(a) == 0 or len(b) == 0:
            return 0
        for word_a in a:
            for word_b in b:
                if word_a == word_b:
                    match += 1
        return match

    @classmethod
    def match_vals(cls, a, b):
        match = 0
        if len(a) == 0 or len(b) == 0:
            return 0
        for word_a in a:
            for word_b in b:
                if word_a == word_b:
                    match += 1
        return match

    @staticmethod
    def match_data(data: dict):
        try:
            arr = []
            for key in [MENTEE_HT, MENTEE_EXP, MENTEE_MAJOR, MENTOR_HT, MENTOR_EXP, MENTOR_MAJOR]:
                if key in data:
                    cleaned = []
                    for rec in data[key]:
                        cleaned.extend(Service.clean(rec))
                    data[key] = cleaned
            for key in [MENTEE_HT, MENTEE_EXP]:
                for k in [MENTOR_HT, MENTOR_EXP, MENTOR_MAJOR]:
                    arr.append(Service.match_vals(data[key], data[k]))
            model = LoadModel.get_model()
            return model.predict(np.array([arr]))[0]
        except (KeyError, ValueError, RuntimeError, RecursionError, TimeoutError) as exp:
            LOGGER.log_err.exception("Error while matching the algo: " + str(exp))
        return 0
