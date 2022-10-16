KOR_VOS_RATE = 1.1
KOR_TAX_RATE = 11

# value of supply
def get_vos(total: float):
    vos = round(total / KOR_VOS_RATE, 0)
    return vos

# tax amount
def get_tax(total: float):
    tax = round(total / KOR_TAX_RATE, 0)
    return tax