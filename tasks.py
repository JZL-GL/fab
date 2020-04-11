from invoke import Collection, task
from task import docs

@task
def mylocaltask(c):
    # Some local stuff goes here
    print(c['sphinx'])

# Add 'docs' to our local root namespace, plus our own task
ns = Collection(mylocaltask, docs)

# Our docs live in 'built_docs', not 'docs/_build'
ns.configure({'sphinx': {'target': "built_docs"}})