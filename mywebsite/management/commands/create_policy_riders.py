from django.core.management.base import BaseCommand
from mywebsite.models import Policy, PolicyRider  # Update 'accounts' to your app name
from faker import Faker
from decimal import Decimal
import random

fake = Faker()

class Command(BaseCommand):
    help = "Generate additional riders (add-ons) for existing policies"

    def handle(self, *args, **kwargs):
        policies = Policy.objects.all()

        if not policies.exists():
            self.stdout.write(self.style.ERROR("❌ No policies found. Please create policies first."))
            return

        rider_pool = [
            "Accidental Death Benefit",
            "Waiver of Premium",
            "Hospital Cash Benefit",
            "Personal Accident Rider",
            "Critical Illness Add-on",
            "Emergency Evacuation Cover",
            "Funeral Expense Cover",
            "Temporary Disability Rider",
            "Maternity Cover",
            "Ambulance Services"
        ]

        created = 0

        for policy in policies:
            num_riders = random.randint(0, 3)
            chosen_riders = random.sample(rider_pool, num_riders)

            for rider_name in chosen_riders:
                coverage_amount = Decimal(random.randint(1000, int(policy.sum_insured / 5)))
                premium_amount = Decimal(random.uniform(100, 1000)).quantize(Decimal("0.01"))

                PolicyRider.objects.create(
                    policy=policy,
                    rider_name=rider_name,
                    coverage_amount=coverage_amount.quantize(Decimal("0.01")),
                    premium_amount=premium_amount,
                    description=fake.sentence(nb_words=12)
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"🎉 Successfully created {created} policy riders."))
