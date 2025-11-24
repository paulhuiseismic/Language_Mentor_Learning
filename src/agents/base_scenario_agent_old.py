class ScenarioAgent:
    def __init__(self):
        self.name = "Scenario Agent"


    def respond(self, user_input: str) -> str:
        raise NotImplementedError("Subclasses must implement this method.")