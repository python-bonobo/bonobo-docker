from functools import partial

import phonenumbers
from faker import Factory

import bonobo

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


graph = get_graph()

if __name__ == '__main__':
    from bonobo.commands.run import get_default_services

    bonobo.run(graph, services=get_default_services(__file__))
