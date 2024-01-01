from sqlmodel.ext.asyncio.session import AsyncSession
from collections import defaultdict

from originations.services.policy.models.policy_rule import PolicyRule


class DataCollectorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def collect(self, rules: list, *args, **kwargs):
        # Build DAG and deduplicate inputs
        dag, all_inputs = self.build_dag(rules)

        # Perform topological sort
        sorted_inputs = self.topological_sort(dag, all_inputs)

        # Collect data using the sorted inputs
        return await self.run_tasks(sorted_inputs, *args, **kwargs)

    def build_dag(self, rules: list[PolicyRule]) -> (defaultdict, set):
        dag = defaultdict(list)
        all_inputs = set()
        for rule in rules:
            for name, input in rule.get_dependancies().items():
                all_inputs.add(input)
                for dep in input.dependencies:
                    dag[dep].append(input)
        return dag, all_inputs

    def topological_sort(self, dag: defaultdict, all_inputs: set):
        visited = set()
        stack = []

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in dag[node]:
                visit(neighbor)
            stack.append(node)

        for input in all_inputs:
            visit(input)

        return stack[::-1]  # Return reversed stack

    async def run_tasks(self, sorted_inputs, *args, **kwargs):
        task_results = {}
        for input in sorted_inputs:
            dependencies_results = [
                task_results[dep] for dep in input.dependencies if dep in task_results
            ]
            data_input = input(self.db)

            await data_input.collect_service_calls(
                data_inputs=dependencies_results, *args, **kwargs
            )

            task_results[input] = data_input
        return task_results
