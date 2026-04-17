class Person:
    """The class Person describes a person."""

    count = 0

    def __init__(self, name: str, dob: str, address: str) -> None:
        """Initialize a Person instance."""
        self.name = name
        self.dob = dob
        self.address = address
        Person.count += 1

    def get_name(self) -> str:
        """Return the person's name."""
        return self.name

    def get_dob(self) -> str:
        """Return the person's date of birth."""
        return self.dob

    def get_address(self) -> str:
        """Return the person's address."""
        return self.address

    def set_name(self, name: str) -> None:
        """Update the person's name."""
        self.name = name

    def set_dob(self, dob: str) -> None:
        """Update the person's date of birth."""
        self.dob = dob

    def set_address(self, address: str) -> None:
        """Update the person's address."""
        self.address = address

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, dob={self.dob!r}, address={self.address!r})"

    def __str__(self) -> str:
        return f"Name: {self.name}\nDOB: {self.dob}\nAddress: {self.address}"

    @classmethod
    def get_count(cls) -> int:
        """Return how many Person instances have been created."""
        return cls.count

p1 = Person ('Amir', '24-10-1990', '38/4, IIT Delhi 110016')
p1.name = 'Jake'
print(p1.get_name())
print(p1)
p2 = Person()
print(p2)
print(Person.get_count())