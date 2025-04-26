class Expense:
    def __init__(self, id, group_id, description, amount, paid_by, date):
        self.id = id
        self.group_id = group_id
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.date = date

    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'description': self.description,
            'amount': self.amount,
            'paid_by': self.paid_by,
            'date': self.date
        }

class Group:
    def __init__(self, id, name, members):
        self.id = id
        self.name = name
        self.members = members

    def add_member(self, member):
        if member not in self.members:
            self.members.append(member)

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'members': self.members
        } 