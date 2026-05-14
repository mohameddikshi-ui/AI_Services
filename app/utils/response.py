import math


def success_response(

    message,

    data,

    page=None,

    pageSize=None,

    total_records=None,

    extra=None
):

    response = {

        "success": True,

        "message": message,

        "data": data
    }

    # ==========================================
    # PAGINATION
    # ==========================================

    if (

        page is not None and

        pageSize is not None and

        total_records is not None
    ):

        response["page"] = page

        response["pageSize"] = pageSize

        response["total_records"] = total_records

        response["total_pages"] = math.ceil(
            total_records / pageSize
        )

    # ==========================================
    # EXTRA METADATA
    # ==========================================

    if extra:

        response.update(extra)

    return response


# ==========================================
# ERROR RESPONSE
# ==========================================

def error_response(

    message,

    error_code="AI_500"
):

    return {

        "success": False,

        "message": message,

        "error_code": error_code
    }