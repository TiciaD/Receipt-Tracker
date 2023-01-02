
import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Receipt
from graphene_file_upload.scalars import Upload


class ReceiptType(DjangoObjectType):
    class Meta:
        model = Receipt

class Query(ObjectType):
    receipt = graphene.Field(ReceiptType, id=graphene.Int())
    receipts = graphene.List(ReceiptType)
    

    def resolve_receipt(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Receipt.objects.get(pk=id)

        return None

    def resolve_receipts(self, info, **kwargs):
        return Receipt.objects.all()


class ReceiptInput(graphene.InputObjectType):
    id = graphene.ID()
    store_name = graphene.String()
    date = graphene.Date()
    cost = graphene.Int()
    tax = graphene.Int()
    image = Upload


class CreateReceipt(graphene.Mutation):
    class Arguments:
        receipt_data = ReceiptInput(required=True)

    # ok = graphene.Boolean()
    receipt = graphene.Field(ReceiptType)

    @staticmethod
    def mutate(root, info, receipt_data=None):
        # ok = True
        receipt_instance = Receipt(
            store_name=receipt_data.store_name,
            date=receipt_data.date,
            cost=receipt_data.cost,
            tax=receipt_data.tax,
            receipt_image=receipt_data.image,
        ) 
        receipt_instance.save()
        return CreateReceipt(receipt=receipt_instance)


# class UpdateReceipt(graphene.Mutation):
#     class Arguments:
#         id = graphene.Int(required=True)
#         input = ReceiptInput(required=True)

#     ok = graphene.Boolean()
#     book = graphene.Field(ReceiptType)

#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         book_ins = Receipt.objects.get(pk=id)
#         if book_ins:
#             ok = True
#             book_ins.title = input.title
#             book_ins.save()
#             return UpdateReceipt(ok=ok, book=book_ins)
#         return UpdateReceipt(ok=ok, book=None)

class Mutation(graphene.ObjectType):
    create_receipt = CreateReceipt.Field()
    # update_receipt = UpdateReceipt.Field()



# schema = graphene.Schema(query=Query)
schema = graphene.Schema(query=Query, mutation=Mutation)