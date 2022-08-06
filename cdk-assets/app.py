from stack.sagemaker_migration_stack import *


app = cdk.App()
SagemakerMigrationStack(app, "SagemakerMigrationStack")
app.synth()
