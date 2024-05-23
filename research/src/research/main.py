#!/usr/bin/env python
import os
import agentops
from dotenv import load_dotenv

load_dotenv()

agentops.init(tags=["research_woodshed"])
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

from research.crew import ResearchCrew

def run():
    inputs = {
        'topic': 'Mindfulness Based Stress Reduction (MBSR)'
    }
    ResearchCrew().crew().kickoff(inputs=inputs)