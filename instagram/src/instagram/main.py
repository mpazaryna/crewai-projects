#!/usr/bin/env python
import datetime
import os

import agentops
from dotenv import load_dotenv

from instagram.crew import InstagramCrew

load_dotenv()

agentops.init(tags=["instagram_example"])
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")


def run():
    inputs = {
        "current_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "instagram_description": "yoga-with-paz",
        "topic_of_the_week": "Mindfulness meditation for those in cancer treatment.",
    }
    InstagramCrew().crew().kickoff(inputs=inputs)
