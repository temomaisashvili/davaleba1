from django.db import models
from django.utils import timezone, timesince
from datetime import datetime


class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=True)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

    @staticmethod
    def username_contains_string(contained_string):
        # TODO: Filter customers where username contains a specific string
        return Customer.objects.filter(username__icontains=contained_string)


    @staticmethod
    def active_customers():
        # TODO: Get all active customers
        return Customer.objects.filter(is_active=True)


    @staticmethod
    def customers_registered_after(date):
        # TODO: Get all customers who registered after a specific date
        return Customer.objects.filter(date_joined__gt=date)


    @staticmethod
    def customer_with_email(email):
        # TODO: Retrieve a customer by email
        return Customer.objects.filter(email=email).first()


    get_full_name.verbose_name = "სრული სახელი"

    class Meta:
        ordering = ("-id",)
        verbose_name = "მომხმარებელი"
        verbose_name_plural = "მომხმარებლები"


class Stadium(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    @staticmethod
    def get_stadium_by_stadium_name(name):
        # TODO: Retrieve a stadium by its name
        return Stadium.objects.filter(name=name).first()


    @staticmethod
    def stadiums_with_capacity_greater_than(capacity):
        # TODO: Get all stadiums with a capacity greater than the specified amount
        return Stadium.objects.filter(capacity__gt=capacity)


    @staticmethod
    def stadiums_in_city(city):
        # TODO: Get all stadiums located in a specific city
        return Stadium.objects.filter(address__icontains=city)


    @staticmethod
    def stadiums_with_events():
        # TODO: Get stadiums that are associated with any event
        pass


class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField("აქტიურია", null=False, default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def event_after_year(year):
        # TODO: Get events occurring after a specific year
        return Event.objects.filter(date__year__gt=year)

    @staticmethod
    def events_at_stadium(stadium_name):
        # TODO: Get all events taking place at a specified stadium
        return Event.objects.filter(stadium__name=stadium_name)


    @staticmethod
    def upcoming_events():
        # TODO: Get all events with a date in the future
        return Event.objects.filter(date__gt=timezone.now())


    @staticmethod
    def active_events():
        # TODO: Get all events that are currently active
        return Event.objects.filter(is_active=True)



class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    bought_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} -- {self.event}"

    @staticmethod
    def tickets_by_customer(customer_id):
        # TODO: Get all tickets bought by a specific customer
        return Ticket.objects.filter(customer_id=customer_id)


    @staticmethod
    def tickets_for_event(event_id):
        # TODO: Get all tickets for a specified event
        return Ticket.objects.filter(event_id=event_id)


    @staticmethod
    def recent_tickets(days=30):
        # TODO: Get all tickets purchased within the last specified number of days
        return Ticket.objects.filter(bought_at__gte=timezone.now() - timezone.timedelta(days=days))


    @staticmethod
    def ticket_count_for_event(event_id):
        # TODO: Get the count of tickets sold for a specific event
        return Ticket.objects.filter(event_id=event_id).count()

