from typing import Literal
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from somewhere import exchange_rate
from myagents import agent, user_proxy

# defines a Pydantic model
class Currency(BaseModel):
  # parameter of type CurrencySymbol
  currency: Annotated[CurrencySymbol, Field(..., description="Currency symbol")]
  # parameter of type float, must be greater or equal to 0 with default value 0
  amount: Annotated[float, Field(0, description="Amount of currency", ge=0)]

@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="Currency exchange calculator.")
def currency_calculator(
  base: Annotated[Currency, "Base currency: amount and currency symbol"],
  quote_currency: Annotated[CurrencySymbol, "Quote currency symbol"] = "USD",
) -> Currency:
  quote_amount = exchange_rate(base.currency, quote_currency) * base.amount
  return Currency(amount=quote_amount, currency=quote_currency)