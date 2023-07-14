
import logging

from openai.error import AuthenticationError, APIConnectionError


def openai_error_handler(func, func_args):
    error_occured = True
    try:
        result = func(func_args)
        error_occured = False
    except ConnectionError:
        result = ':red[Failed to Connect]'
    except ValueError as e:
        logging.exception(e)
        result = f':red[{e}]'
    except AuthenticationError as e:
        logging.exception(e)
        result = f':red[Invalid API Key]'
    except APIConnectionError as e:
        logging.exception(e)
        result = f':red[Error communicating with OpenAI]'
    except Exception as e:
        logging.exception(e)
        result = f':red[{e}]'
    finally:
        return {'result': result, "error_occured": error_occured}
