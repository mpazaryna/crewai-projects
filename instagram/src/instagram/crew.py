from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from instagram.tools.search import SearchTools


@CrewBase
class InstagramCrew:
    """Instagram crew"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o"
            # model="gpt-4-turbo"
            # model="gpt-3.5-turbo"
        )

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_researcher"],
            tools=[
                SearchTools.search_internet,
                SearchTools.search_instagram,
                SearchTools.open_page,
            ],
            verbose=True,
            agent=self.llm,
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["content_strategist"], verbose=True, llm=self.llm
        )

    # @agent
    # def visual_creator(self) -> Agent:
    #    return Agent(
    #        config=self.agents_config["visual_creator"],
    #        verbose=True,
    #        allow_delegation=False,
    #        llm=self.llm,
    #    )

    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config["copywriter"], verbose=True, llm=self.llm
        )

    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_research"],
            agent=self.market_researcher(),
            output_file="market_research.md",
        )

    # @task
    # def content_strategy_task(self) -> Task:
    #    return Task(
    #        config=self.tasks_config["content_strategy"],
    #        agent=self.content_strategist(),
    #    )

    # @task
    # def visual_content_creation_task(self) -> Task:
    #    return Task(
    #        config=self.tasks_config["visual_content_creation"],
    #        agent=self.visual_creator(),
    #        output_file="visual-content.md",
    #    )

    @task
    def copywriting_task(self) -> Task:
        return Task(
            config=self.tasks_config["copywriting"],
            agent=self.copywriter(),
            output_file="copywriting.md",
        )

    @task
    def report_final_content_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["report_final_content_strategy"],
            agent=self.content_strategist(),
            output_file="final-content-strategy.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Instagram crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
