from fastapi import APIRouter, Depends
from src.tools.jobs import job_btc, job_eth, job_dca
from src.api.dependencies import require_api_token
from src.api.models.trade_models import TradeRequest, DcaRequest

router = APIRouter(
    prefix="/trades",
    tags=["Trades"],
    # dependencies=[Depends(require_api_token)],
)


@router.post("/btc")
def trade_btc(request: TradeRequest):
    result = job_btc(request.amount)
    return {
        "status": "submitted",
        "asset": "BTC",
        "eur_amount": request.amount,
        "kraken_result": result,
    }


@router.post("/eth")
def trade_eth(request: TradeRequest):
    result = job_eth(request.amount)

    return {
        "status": "submitted",
        "asset": "ETH",
        "eur_amount": request.amount,
        "kraken_result": result,
    }


@router.post("/dca")
def trade_dca(request: DcaRequest):
    result = job_dca(
        btc_amount=request.btc_amount,
        eth_amount=request.eth_amount,
    )

    return {
        "status": "submitted",
        "result": result,
    }