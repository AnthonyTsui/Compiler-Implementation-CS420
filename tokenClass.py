class token:
    def __init__(self, token_val, token_type, token_action):
        self.token_val = token_val
        self.token_type = token_type
        self.token_action = token_action
    
    def get_val(self):
        return self.token_val

    def get_type(self):
        return self.token_type

    def get_action(self):
        return self.token_action

    