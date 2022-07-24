import abc

class RFServerInterface(metaclass = abc.ABCMeta):

    @abc.abstractmethod
    def get_keyword_request(self, *args, **kwargs) -> dict:
        pass


    @abc.abstractmethod
    def send_keyword_result(self, result: dict, kw_dict: dict) -> dict:
        pass

