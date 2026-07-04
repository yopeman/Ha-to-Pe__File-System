from ariadne import ObjectType

payment_type = ObjectType("Payment")

@payment_type.field("id")
def resolve_payment_id(payment_obj, info):
    return payment_obj.id

@payment_type.field("user_id")
def resolve_user_id(payment_obj, info):
    return payment_obj.user_id

@payment_type.field("amount")
def resolve_amount(payment_obj, info):
    return payment_obj.amount

@payment_type.field("currency")
def resolve_currency(payment_obj, info):
    return payment_obj.currency

@payment_type.field("status")
def resolve_status(payment_obj, info):
    return payment_obj.status.name

@payment_type.field("transaction_id")
def resolve_transaction_id(payment_obj, info):
    return payment_obj.transaction_id

@payment_type.field("created_at")
def resolve_created_at(payment_obj, info):
    return payment_obj.created_at

@payment_type.field("updated_at")
def resolve_updated_at(payment_obj, info):
    return payment_obj.updated_at

@payment_type.field("paid_at")
def resolve_paid_at(payment_obj, info):
    return payment_obj.paid_at