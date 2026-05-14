def get_pagination(page: int, pageSize: int):
    if page < 1:
        page = 1
    if pageSize < 1:
        pageSize = 10

    offset = (page - 1) * pageSize
    return offset, pageSize