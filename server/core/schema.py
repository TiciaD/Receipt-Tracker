import graphene
import receipts.schema

class Query(receipts.schema.Query, graphene.ObjectType):
    pass
class Mutation(receipts.schema.Mutation, graphene.ObjectType):
    pass
schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query)
