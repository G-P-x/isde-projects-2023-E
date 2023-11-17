class result_storage:
    def __init__(self, classification_results = None) -> None:
        self._classification_results = classification_results
        
    @property
    def classification_results(self):
        return self._classification_results

    @classification_results.setter
    def classification_results(self, value):
        if not isinstance(value, dict) and value is not None:
            raise TypeError("Expected a dictionary")
        self._classification_results = value
        
    def generate_JSON(self, classification_score: list):
        json = {}
        for el in classification_score:
            if not isinstance(el, list):
                raise TypeError("Expected a list")
            json[el[0]] = el[1]
        self.classification_results = json
        