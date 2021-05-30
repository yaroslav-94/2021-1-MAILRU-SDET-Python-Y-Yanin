from faker import Factory


class Generator:

    def create_user_name(self) -> list:
        fake = Factory.create('it_IT')
        return fake.name().split(" ")[0:2]
