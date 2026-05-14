# import logging

# from logging.handlers import RotatingFileHandler


# # ==========================================
# # LOGGER CONFIG
# # ==========================================

# logger = logging.getLogger("ai_service")

# logger.setLevel(logging.INFO)


# # ==========================================
# # FORMAT
# # ==========================================

# formatter = logging.Formatter(

#     "%(asctime)s | %(levelname)s | %(message)s"
# )


# # ==========================================
# # FILE HANDLER
# # ==========================================

# file_handler = RotatingFileHandler(

#     "app.log",

#     maxBytes=5 * 1024 * 1024,

#     backupCount=5
# )

# file_handler.setFormatter(formatter)


# # ==========================================
# # CONSOLE HANDLER
# # ==========================================

# console_handler = logging.StreamHandler()

# console_handler.setFormatter(formatter)


# # ==========================================
# # ADD HANDLERS
# # ==========================================

# logger.addHandler(file_handler)

# logger.addHandler(console_handler)



# latter venumna logger use pannalam