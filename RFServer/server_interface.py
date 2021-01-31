import abc

class RFServerInterface(metaclass = abc.ABCMeta):
    
    @abc.abstractmethod
    def get_keyword_request(self, *args, **kwargs) -> dict:
        pass

    
    @abc.abstractmethod
    def send_keyword_result(self, result: dict) -> dict:
        pass





if __name__ == "__main__":
    class Test(RFServerInterface):
        
        def get_keyword_request(self):
            return {'test':'1111'}


        def send_keyword_result(self, result):
            return (result, 'ready')
    

    breakpoint()
    
