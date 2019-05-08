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

    
    def is_add_sub(self):
        addsub = ['+', '-']
        if self.token_val in addsub:
            return True
        return False

    def is_mult_div_op(self):
        divOps = ['*', '/', '%']
        if self.token_val in divOps:
            return True
        return False

    def is_unary_op(self):
        unaryOps = ['+', '-', 'or']
        if self.token_val in unaryOps:
            return True
        return False

    def is_relation_op(self):
        relateOps = ['=', '<>', '<', '>', '<=', '>=']
        if self.token_val in relateOps:
            return True
        return False

    def is_io_op(self):
        ioOps = ['TOKEN_WRITELN']
        if self.token_type in ioOps:
            return True
        return False

    def __repr__(self):
       #DEBUGGING purposes
        tk_str = "{TOKEN_VAL: %s \t TOKEN_TYPE: %s \t TOKEN_ACTION: %s}" % (
                self.get_val(),
                self.get_type(),
                self.get_action()
                )

        return tk_str

    