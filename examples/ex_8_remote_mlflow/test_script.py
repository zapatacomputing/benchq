import orquestra.sdk as sdk

wf = sdk.WorkflowRun.by_id("mlflow_example_workflow-qkwjy-r000")

tasks = wf.get_artifacts()

print(tasks)

# for task in tasks:
#     if task.task_invocation_id == "invocation-0-task-gsc-estimates":
#         breakpoint()
