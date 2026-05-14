from pydantic import BaseModel, ConfigDict, Field


class TradeRequest(BaseModel):
    amount: float = Field(
        gt=0,
        le=10000,
        multiple_of=0.01,
        description="EUR amount to invest, EURO"
    )
    model_config = ConfigDict(extra= "forbid")

class DcaRequest(BaseModel):
    btc_amount: float = Field(
        gt=0,
        le=10000,
        multiple_of=0.01,
        description="EUR amount to invest in BTC"
    )
    eth_amount: float = Field(
        gt=0,
        le=10000,
        multiple_of=0.01,
        description="EUR amount to invest in ETH"
    )

    model_config = ConfigDict(extra="forbid")


