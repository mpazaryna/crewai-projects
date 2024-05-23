from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

@CrewBase
class ResearchCrew():
	"""Research crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
	def __init__(self):
		# self.llm = ChatOpenAI(
        	# model="gpt-4o"
    		# model="gpt-4-turbo"
        #)
		self.llm = ChatGroq(
			# model="mixtral-8x7b-32768"
			# model="llama3-8b-8192"
			# model="llama3-70b-8192"
			model="gemma-7b-it"
		)	

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=self.llm,
			# max_iter=4,
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			llm=self.llm,
			# max_iter=4,
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher(),
			output_file='research.md'
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # https://docs.crewai.com/how-to/Hierarchical/
		)