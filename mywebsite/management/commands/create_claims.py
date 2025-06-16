from django.core.management.base import BaseCommand
from mywebsite.models import Claim, Policy, User  # Update with your actual app and model paths
from faker import Faker
from decimal import Decimal
import random
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = "Generate sample insurance claims"

    def handle(self, *args, **kwargs):
        policies = list(Policy.objects.all())
        users = list(User.objects.all())

        if not policies:
            self.stdout.write(self.style.ERROR("❌ No policies found. Create policies first."))
            return

        claim_types = [
            'total_loss', 'partial_loss', 'theft', 'accident',
            'medical', 'death', 'disability', 'property_damage', 'other'
        ]
        statuses = [
            'reported', 'investigating', 'processing',
            'approved', 'declined', 'settled', 'closed'
        ]

        for i in range(100):
            policy = random.choice(policies)
            assigned_to = random.choice(users)
            claim_type = random.choice(claim_types)
            status = random.choice(statuses)

            incident_date = fake.date_between(start_date='-2y', end_date='today')
            claimed_amount = Decimal(random.randint(5000, 500000))
            assessed_amount = claimed_amount * Decimal(random.uniform(0.6, 1.0))
            approved_amount = assessed_amount if status in ['approved', 'settled', 'closed'] else Decimal(0)
            paid_amount = approved_amount if status in ['settled', 'closed'] else Decimal(0)

            claim = Claim.objects.create(
                claim_number=f"CLM{100000 + i}",
                policy=policy,
                claim_type=claim_type,
                status=status,
                incident_date=incident_date,
                incident_description=fake.text(max_nb_chars=200),
                incident_location=fake.address(),
                police_report_number=fake.bothify(text='PR##??##'),
                claimed_amount=claimed_amount.quantize(Decimal('0.01')),
                assessed_amount=assessed_amount.quantize(Decimal('0.01')),
                approved_amount=approved_amount.quantize(Decimal('0.01')),
                paid_amount=paid_amount.quantize(Decimal('0.01')),
                assigned_to=assigned_to,
                surveyor=fake.name() if random.choice([True, False]) else '',
                surveyor_report=fake.text(max_nb_chars=100) if random.choice([True, False]) else '',
                decline_reason=fake.sentence(nb_words=6) if status == 'declined' else ''
            )

            self.stdout.write(self.style.SUCCESS(f"✅ Created claim {claim.claim_number}"))

        self.stdout.write(self.style.SUCCESS("🎉 100 insurance claims created successfully."))
