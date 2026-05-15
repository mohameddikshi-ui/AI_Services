def get_pagination(page: int, pageSize: int):

    # ==========================================
    # SAFE PAGE DEFAULT
    # ==========================================

    if page < 1:

        page = 1

    # ==========================================
    # SAFE PAGE SIZE DEFAULT
    # ==========================================

    if pageSize < 1:

        pageSize = 10

    # ==========================================
    # MAX PAGE SIZE PROTECTION
    # ==========================================

    if pageSize > 100:

        pageSize = 100

    # ==========================================
    # OFFSET CALCULATION
    # ==========================================

    offset = (page - 1) * pageSize

    return offset, pageSize