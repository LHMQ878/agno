"""
AirflowTools - DAG file management.

pip install apache-airflow
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.airflow import AirflowTools

# Example 1: All functions enabled (default)
agent_full = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[AirflowTools(dags_dir="tmp/dags")],
)

# Example 2: Read-only (disable save)
agent_readonly = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[
        AirflowTools(
            dags_dir="tmp/dags",
            save_dag_file=False,
            read_dag_file=True,
        )
    ],
)

# Example 3: Enable all explicitly
agent_all = Agent(
    model=OpenAIResponses(id="gpt-4.1"),
    tools=[AirflowTools(dags_dir="tmp/dags", all=True)],
)

agent = agent_full

dag_content = """
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'example_dag',
    default_args=default_args,
    description='A simple example DAG',
    schedule='@daily',
    catchup=False
) as dag:

    def print_hello():
        print("Hello from Airflow!")
        return "Hello task completed"

    task = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello,
        dag=dag,
    )
"""

if __name__ == "__main__":
    agent.run(f"Save this DAG file as 'example_dag.py': {dag_content}")
    agent.print_response("Read the contents of 'example_dag.py'")
