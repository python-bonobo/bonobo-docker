import bonobo
import phonenumbers

from faker import Factory
from functools import partial

fake = Factory.create('fr_FR')

NUMBERS = [fake.phone_number() for i in range(100)]


def get_graph():
    graph = bonobo.Graph(
        NUMBERS,
        partial(phonenumbers.parse, region='FR'),
        partial(phonenumbers.format_number, num_format=phonenumbers.PhoneNumberFormat.E164),
        print,
    )

    return graph


if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(get_graph(**options))
