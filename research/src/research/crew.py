import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


@CrewBase
class ResearchCrew:
    """Research crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):

        # OpenAI models
        self.gpt3 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.gpt4 = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.7)
        self.gpt4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

         # Groq Models
        self.llama3_8b = ChatGroq(temperature=0.7,  model_name="llama3-8b-8192")
        self.llama3_70b = ChatGroq(temperature=0.7,  model_name="llama3-70b-8192")
        self.mixtral_8x7b = ChatGroq(temperature=0.7,  model_name="mixtral-8x7b-32768")
        self.gemma_7b = ChatGroq(temperature=0.7,  model_name="gemma-7b-it")
        
        agent_model = os.getenv("AGENT_MODEL")
        if agent_model == "ChatOpenAI":
            self.llm = self.gpt4o
        elif agent_model == "ChatGroq":
            self.llm = self.llama3_70b
        elif agent_model == "Ollama":
            self.llm = Ollama(model="mistral")
        else:
            raise ValueError("Invalid AGENT_MODEL environment variable value")

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            verbose=True,
            llm=self.llm,
            system_template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{{ .System }}<|eot_id|>""",
            prompt_template="""<|start_header_id|>user<|end_header_id|>{{ .Prompt }}<|eot_id|>""",
            response_template="""<|start_header_id|>assistant<|end_header_id|>{{ .Response }}<|eot_id|>""",
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            verbose=True,
            llm=self.llm,
            system_template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{{ .System }}<|eot_id|>""",
            prompt_template="""<|start_header_id|>user<|end_header_id|>{{ .Prompt }}<|eot_id|>""",
            response_template="""<|start_header_id|>assistant<|end_header_id|>{{ .Response }}<|eot_id|>""",

        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            output_file="research.md",
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
            agent=self.reporting_analyst(),
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # https://docs.crewai.com/how-to/Hierarchical/
        )
