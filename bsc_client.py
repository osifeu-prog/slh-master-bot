import httpx

async def get_token_price():
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get("https://api.coingecko.com/api/v3/simple/price?ids=binancecoin&vs_currencies=usd")
            data = resp.json()
            bnb_usd = data["binancecoin"]["usd"]
            slh_bnb = 0.000005
            slh_usd = round(bnb_usd * slh_bnb, 6)
            return {"slh_bnb": slh_bnb, "bnb_usd": bnb_usd, "slh_usd": slh_usd}
    except:
        return None
