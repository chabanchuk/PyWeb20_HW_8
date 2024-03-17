import json
from faker import Faker
from mongoengine.errors import NotUniqueError
from models import Author, Quote, Contact

fake = Faker()

def seed_authors():
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує: {el.get('fullname')}")

def seed_quotes():
    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author_name = el.get('author')
            author = Author.objects(fullname=author_name).first()
            if author:
                quote_text = el.get('quote')
                existing_quote = Quote.objects(quote=quote_text).first()
                if not existing_quote:
                    quote = Quote(quote=quote_text, tags=el.get('tags'), author=author)
                    quote.save()
                else:
                    print(f"Цитата вже існує: '{quote_text}'")
            else:
                print(f"Автор не знайдений: {author_name}")

def seed_contacts(num_contacts):
    for _ in range(num_contacts):
        try:
            contact = Contact(
                full_name=fake.name(),
                email=fake.email(),
                phone_number=fake.phone_number()[:15],
                prefer_sms=fake.boolean(chance_of_getting_true=50),
                message_sent=fake.boolean(chance_of_getting_true=50),
                address=fake.address()
            )
            contact.save()
        except NotUniqueError:
            pass

if __name__ == '__main__':
    seed_authors()
    seed_quotes()
    seed_contacts(10)
    print("База даних успішно створена.")


    