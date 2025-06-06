# Config/shared.py 

import os
import sys  

from dotenv import load_dotenv
from typing import List, Dict

from pydantic import BaseModel, Field

import google.generativeai as genai

from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

import agentops

from tavily import TavilyClient
import sys
