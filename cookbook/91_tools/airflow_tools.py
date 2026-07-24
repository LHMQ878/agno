"""
AirflowTools - DAG file management.

pip install apache-airflow
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.airflow import AirflowTools

agent = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[AirflowTools(dags_dir="tmp/dags")],
)

dag_content = """
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG("example_dag", start_date=datetime(2024, 1, 1), schedule="@daily") as dag:
    PythonOperator(task_id="hello", python_callable=lambda: print("Hello"))
"""

if __name__ == "__main__":
    agent.print_response(f"Save this DAG as 'example_dag.py': {dag_content}")
    agent.print_response("Read 'example_dag.py'")
