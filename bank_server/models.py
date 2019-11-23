import uuid


class Response(object):

    def __init__(self, code=None, description=None):

        self.swagger_types = {
            'code': int,
            'description': str
        }

        self.attribute_map = {
            'code': 'code',
            'description': 'description'
        }

        self._code = code
        self._description = description

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")

        self._code = code

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")

        self._description = description

    def serialize(self):
        return {
            "code": self._code,
            "description": self._description
        }


class UniqueBankRequest(object):

    def __init__(self, identifier=None, amount=None, operation=None):

        self.swagger_types = {
            'amount': int,
            'operation': str,
            'id': int
        }

        self.attribute_map = {
            'amount': 'amount',
            'operation': 'operation',
            'id': 'identifier'
        }

        self._id = identifier
        self._amount = amount
        self._operation = operation

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")
        if amount is not None and amount > 50000:
            raise ValueError("Invalid value for `amount`, must be a value less than or equal to `50000`")
        if amount is not None and amount < 10000:
            raise ValueError("Invalid value for `amount`, must be a value greater than or equal to `10000`")

        self._amount = amount

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, operation):
        allowed_values = ["CREDIT", "DEBIT"]
        if operation not in allowed_values:
            raise ValueError(
                "Invalid value for `operation` ({0}), must be one of {1}".format(operation, allowed_values)
            )

        self._operation = operation

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, identifier):
        if identifier is not None and identifier < 1:
            raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")

        self._id = identifier

    def serialize(self):
        return {
            "id": self._id,
            "amount": self._amount,
            "operation": self._operation
        }

    def deserialize(self, data):
        if not isinstance(data, dict):
            raise ValueError('Invalid unique bank request: body of request contained bad or no data')
        try:
            self._id = data['id']
            self._amount = data['amount']
            self._operation = data['operation']
        except KeyError as e:
            raise ValueError('Invalid bank request: missing ' + e.args[0])
        return


class UBRList(object):

    def __init__(self):
        self.swagger_types = {
        }

        self.attribute_map = {
        }

        self._list = []

    def deserialize(self, data):
        if not isinstance(data, list):
            raise ValueError('Invalid sequence of unique bank requests: object contained bad or no data')
        for ubr in data:
            obj = UniqueBankRequest()
            obj.deserialize(ubr)
            self._list.append(obj)

    def get_sorted(self):
        return sorted(self._list, key=lambda ubr: ubr.id)


class Account(object):

    def __init__(self, identifier=None, balance=None):

        if identifier is None:
            identifier = uuid.uuid4().hex

        if balance is None:
            balance = 0

        self.swagger_types = {
            'id': str,
            'balance': int
        }

        self.attribute_map = {
            'id': 'identifier',
            'balance': 'balance'
        }

        self._id = identifier
        self._balance = balance

    @property
    def id(self):
        return self._id

    @property
    def balance(self):
        return self._balance

    def increase_balance(self, amount):
        if not isinstance(amount, int):
            raise ValueError('Invalid input: amount must be a number')
        if amount <= 0:
            raise ValueError('Invalid input: amount must be positive number')

        self._balance += amount

    def decrease_balance(self, amount):
        if not isinstance(amount, int):
            raise ValueError('Invalid input: amount must be a number')
        if amount <= 0:
            raise ValueError('Invalid input: amount must be positive number')
        if self._balance <= 0:
            raise ValueError('Cannot perform operation: there is no money in the account')

        self._balance -= amount

    def serialize(self):
        return {
            "id": self._id,
            "balance": self._balance
        }
