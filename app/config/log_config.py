import logging
import os


# Configuração do logger
logger = logging.getLogger("pipeline_logger")
logger.setLevel(logging.DEBUG)

# Formato do log
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Limpa handlers para evitar duplicação
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(console_handler)

# Evita propagação para o logger raiz, que pode imprimir duplicado
logger.propagate = False