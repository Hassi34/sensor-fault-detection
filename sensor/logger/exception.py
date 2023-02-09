import sys 

def error_message_detail(error, error_detail :sys):
    _, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = f"Error occurred with python script name [{file_name}] at line number [{exc_tb.tb_lineno}] with error message [{str(error)}]"
    return error_message

class SensorException(Exception):
    def __init__(self, error_message, error_detail: sys):
        """gets the error message and the detail

        Args:
            error_message (str): error message
            error_detail (str): error detail
        """        
        super().__init__(error_message)

        self.error_message = error_message_detail(error_message, error_detail = error_detail )

    def __str__(self):
        return self.error_message
